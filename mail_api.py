
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("TEMPMAIL_API_TOKEN")
BASE_URL = "https://tempmail.id.vn/api"

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

def create_email(username=None, domain="tempmail.id.vn"):
    data = {}
    if username:
        data["user"] = username
        data["domain"] = domain
    return requests.post(f"{BASE_URL}/email/create", json=data, headers=HEADERS).json()

def list_emails():
    return requests.get(f"{BASE_URL}/email", headers=HEADERS).json()

def get_email_inbox(mail_id):
    return requests.get(f"{BASE_URL}/email/{mail_id}", headers=HEADERS).json()

def read_message(message_id):
    return requests.get(f"{BASE_URL}/message/{message_id}", headers=HEADERS).json()
