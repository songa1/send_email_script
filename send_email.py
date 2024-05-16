from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import smtplib


def send_email(subject, body, to_email, attachment_path):
    # Set up the email server and login credentials
    smtp_server = "<email_server>"
    smtp_port = 587
    smtp_username = "<sending_email>"
    smtp_password = "<email_password>"

    # Create the MIME object
    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach the body text
    msg.attach(MIMEText(body, "plain"))

    # Attach the file
    attachment_filename = os.path.basename(attachment_path)
    attachment = open(attachment_path, "rb")

    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {attachment_filename}")

    msg.attach(part)

    # Connect to the server and send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, to_email, msg.as_string())
    server.quit()

if __name__ == "__main__":
    subject = "<email_subject>"
    body = "<body>"
    to_email = "<receiving_email>"
    attachment_path = "<attachment_path>"

    send_email(subject, body, to_email, attachment_path)