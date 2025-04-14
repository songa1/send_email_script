#!/usr/bin/env python3

import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate

# =======================
# Configuration Variables
# =======================
BACKUP_FOLDER = "/root/BACKUP"
SMTP_SERVER = "<email_server>"
SMTP_PORT = <server_port>
SMTP_USERNAME = "<email_username>"
SMTP_PASSWORD = "<email_pass>"

TO_EMAIL = "<recipient_email>"
EMAIL_SUBJECT = "This is a backup file"
EMAIL_BODY = "Attached is the most recent YALI AMS backup file."

FILE_EXTENSION = ".sql"  # Change to ".gz" if needed


def find_latest_file(folder_path, extension):
    files = [f for f in os.listdir(folder_path) if f.endswith(extension)]
    if not files:
        raise FileNotFoundError(f"No '{extension}' files found in {folder_path}")
    latest = max(files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
    return os.path.join(folder_path, latest)


def send_email(subject, body, to_email, attachment_path):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    filename = os.path.basename(attachment_path)
    with open(attachment_path, "rb") as file:
        part = MIMEApplication(file.read(), Name=filename)
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        print(f"✅ Email sent successfully with attachment: {filename}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


if __name__ == "__main__":
    try:
        latest_file = find_latest_file(BACKUP_FOLDER, FILE_EXTENSION)
        send_email(EMAIL_SUBJECT, EMAIL_BODY, TO_EMAIL, latest_file)
    except Exception as err:
        print(f"❌ Error: {err}")
