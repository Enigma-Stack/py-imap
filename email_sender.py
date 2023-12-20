import smtplib
import ssl
import os
import logging
import main
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_email_with_attachment(to, bodyUuid, attachmentUuid, attachmentFilePath = '', body='', subject="No Subject", encryption_flag="0"):
    smtp_server = main.HOST
    port = main.PORT

    sender_email = main.EMAIL
    receiver_email = to # email_details.get('to')
    password = main.PASSWORD 

    logging.info("Creating MIME message for email.")
    message = MIMEMultipart("mixed")
    message["Subject"] = subject #email_details.get('subject', 'No Subject')
    message["From"] = sender_email
    message["To"] = receiver_email

    # Add encryption headers
    encryption = encryption_flag #email_details.get('encryption', '0')
    if encryption == "1":
        # OTP Encryption
        message.add_header("X-Body-Encryption", "OTP")
        message.add_header("X-Body-UUID", bodyUuid) # email_details['bodyUuid'])
        message.add_header("X-Attachment-Encryption", "OTP")
        message.add_header("X-Attachment-UUID", attachmentUuid)#email_details['attachmentUuid'])
    elif encryption == "2":
        # AES Encryption
        message.add_header("X-Body-Encryption", "AES")
        message.add_header("X-Body-UUID", "AES")
        message.add_header("X-Attachment-Encryption", "AES")
        message.add_header("X-Attachment-UUID", "AES")
    # Add more conditions for other types of encryption if needed

    # Add body
    body = MIMEText(body, "plain")
    message.attach(body)

    # Add attachment
    if attachmentFilePath:
        logging.info("Attaching file to email.")
        filename = os.path.basename(attachmentFilePath)
        with open(attachmentFilePath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")
        message.attach(part)

    # Send email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            logging.info("Logging into email server.")
            server.login(sender_email, password)
            logging.info("Sending email.")
            server.sendmail(sender_email, receiver_email, message.as_string())
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error("Error sending email: %s", e)
        raise

# Example usage (Uncomment to test directly from this module)
# email_details = {
#     'to': 'recipient@example.com',
#     'subject': 'Test Email',
#     'body': 'This is a test email with attachment.',
#     'attachmentFilePath': '/path/to/your/attachment',
#     'attachmentMimeType': 'image/png',  # or the correct MIME type
#     'attachmentFileName': 'test.png',
#     'encryption': '0',  # Assuming no encryption for this example
#     'bodyUuid': '',
#     'attachmentUuid': '',
# }
# send_email_with_attachment(email_details)
# flag_attachment
