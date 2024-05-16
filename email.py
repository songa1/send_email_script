from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os
import smtplib

folder_path = os.path.expanduser("<directory>")
latest_file = max([f for f in os.listdir(folder_path) if f.endswith('.gz')], key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
latest_file_path = os.path.join(folder_path, latest_file)

def send_email(subject, body, to_email, attachment_path):
    # Set up the email server and login credentials
    smtp_server = "<server>"
    smtp_port = 587
    smtp_username = "<sender_email>"
    smtp_password = "<email_pass>"

    # Create the MIME object
    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = to_email
    msg["Subject"] = subject

    with open(latest_file_path, 'rb') as file:
        part = MIMEApplication(file.read(), Name=latest_file)

    part['Content-Disposition'] = f'attachment; filename="{latest_file}"'
    msg.attach(part)

    # Attach the body text
    msg.attach(MIMEText(body, "plain"))

    # Attach the file
    attachment = open(latest_file_path, "rb")

    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {latest_file}")

    msg.attach(part)

    # Connect to the server and send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, to_email, msg.as_string())
    server.quit()

if __name__ == "__main__":
    subject = "<email_subject>"
    body = "<email_body>"
    to_email = "<email_receiving>"
    attachment_path = latest_file_path

    send_email(subject, body, to_email, attachment_path)