import json
import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

import mail_api

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATA_FILE = "user_data.json"

logging.basicConfig(level=logging.INFO)

def load_user_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

user_data = load_user_data()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📬 Tạo mail mới", callback_data="create_mail")],
        [InlineKeyboardButton("📥 Hộp thư đến", callback_data="inbox")]
    ]
    await update.message.reply_text(
        "🧙‍♂️ Chào mừng đến với bot mail ảo!\nChọn chức năng:", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)

    if query.data == "create_mail":
        res = mail_api.create_email()
        email = res.get("email")
        mail_id = res.get("id")
        user_data[user_id] = {"email": email, "mail_id": mail_id}
        save_user_data(user_data)
        await query.edit_message_text(f"✅ Email của bạn: {email}")

    elif query.data == "inbox":
        if user_id not in user_data:
            await query.edit_message_text("❌ Bạn chưa tạo mail. Hãy chọn 'Tạo mail mới' trước.")
            return
        mail_id = user_data[user_id]["mail_id"]
        inbox = mail_api.get_email_inbox(mail_id)
        messages = inbox.get("data", [])
        if not messages:
            await query.edit_message_text("📭 Hộp thư trống.")
            return
        text = "📨 Thư mới:\n"
        for msg in messages[:5]:
            text += f"- {msg.get('from')} | {msg.get('subject')}\n"
        await query.edit_message_text(text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
