from googleapiclient.discovery import build
from backend.auth.google_auth import authenticate_gmail
import base64
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

USER_EMAIL = os.getenv("USER_EMAIL")

class GmailTool:
    def __init__(self):
        creds = authenticate_gmail()
        self.service = build("gmail", "v1", credentials=creds)

    def get_labels(self):
        results = self.service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            return "No labels found."

        return [label["name"] for label in labels]
    
    def get_recent_emails(self, max_results=5):
        results = self.service.users().messages().list(
            userId="me",
            # labelIds=["INBOX"],  # Disabled for testing
            q="-from:me",
            maxResults=max_results
        ).execute()

        messages = results.get("messages", [])

        if not messages:
            return []

        email_data = []

        for msg in messages:
            message = self.service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["Subject", "From", "To"]
            ).execute()

            headers = message.get("payload", {}).get("headers", [])

            subject = "No Subject"
            sender = "Unknown Sender"
            recipient = "Unknown Recipient"

            for header in headers:
                if header["name"].lower() == "subject":
                    subject = header["value"]
                elif header["name"].lower() == "from":
                    sender = header["value"]
                elif header["name"].lower() == "to":
                    recipient = header["value"]

            # Only include emails actually addressed to this account
            if USER_EMAIL.lower() not in recipient.lower():
                continue

            sender_lower = sender.lower()

            # Exclude automated/system-generated emails
            if (
                "mailer-daemon" in sender_lower or
                "mail delivery subsystem" in sender_lower or
                "no-reply" in sender_lower
            ):
                continue
            
            email_data.append({
                "sender": sender,
                "recipient": recipient,
                "subject": subject
            })

        return email_data
    
    def send_email(self, to, subject, body):
        message = MIMEText(body)

        message["to"] = to
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        send_message = {
            "raw": raw_message
        }

        try:
            sent_message = self.service.users().messages().send(
                userId="me",
                body=send_message
            ).execute()

            return {
                "status": "success",
                "message_id": sent_message["id"]
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def search_emails_by_sender(self, sender_email, max_results=5):
        query = f"from:{sender_email}"

        results = self.service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get("messages", [])

        if not messages:
            return []

        email_data = []

        for msg in messages:
            message = self.service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["Subject", "From", "Date"]
            ).execute()

            headers = message.get("payload", {}).get("headers", [])

            subject = "No Subject"
            sender = "Unknown Sender"
            date = "Unknown Date"

            for header in headers:
                if header["name"].lower() == "subject":
                    subject = header["value"]
                elif header["name"].lower() == "from":
                    sender = header["value"]
                elif header["name"].lower() == "date":
                    date = header["value"]

            email_data.append({
                "sender": sender,
                "subject": subject,
                "date": date
            })

        return email_data

    def search_emails_by_subject(self, subject_keyword, max_results=5):
        query = f"subject:{subject_keyword}"

        results = self.service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get("messages", [])

        if not messages:
            return []

        email_data = []

        for msg in messages:
            message = self.service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["Subject", "From", "Date"]
            ).execute()

            headers = message.get("payload", {}).get("headers", [])

            subject = "No Subject"
            sender = "Unknown Sender"
            date = "Unknown Date"

            for header in headers:
                if header["name"].lower() == "subject":
                    subject = header["value"]
                elif header["name"].lower() == "from":
                    sender = header["value"]
                elif header["name"].lower() == "date":
                    date = header["value"]

            email_data.append({
                "sender": sender,
                "subject": subject,
                "date": date
            })

        return email_data

    def create_draft_email(self, to, subject, body):
        message = MIMEText(body)

        message["to"] = to
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        draft_body = {
            "message": {
                "raw": raw_message
            }
        }

        try:
            draft = self.service.users().drafts().create(
                userId="me",
                body=draft_body
            ).execute()

            return {
                "status": "success",
                "draft_id": draft["id"],
                "message": "Draft created successfully"
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def list_drafts(self, max_results=10):
        results = self.service.users().drafts().list(
            userId="me",
            maxResults=max_results
        ).execute()

        drafts = results.get("drafts", [])

        if not drafts:
            return []

        draft_data = []

        for draft in drafts:
            draft_detail = self.service.users().drafts().get(
                userId="me",
                id=draft["id"]
            ).execute()

            headers = draft_detail["message"]["payload"]["headers"]

            subject = "No Subject"
            recipient = "Unknown Recipient"

            for header in headers:
                if header["name"].lower() == "subject":
                    subject = header["value"]
                elif header["name"].lower() == "to":
                    recipient = header["value"]

            draft_data.append({
                "draft_id": draft["id"],
                "recipient": recipient,
                "subject": subject
            })

        return draft_data

    def send_draft(self, draft_id):
        try:
            sent_draft = self.service.users().drafts().send(
                userId="me",
                body={
                    "id": draft_id
                }
            ).execute()

            return {
                "status": "success",
                "message_id": sent_draft["id"],
                "message": "Draft sent successfully"
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }