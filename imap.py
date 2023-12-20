import imaplib
import email
from email.header import decode_header
import base64

class EncryptionInfo:
    def __init__(self):
        self.flag = 0  # Default to no encryption
        self.bodyUuid = None
        self.attachmentUuid = None

class EmailObject:
    def __init__(self, subject, body, attachments, from_, to, cc, bcc, headers, date, encryption):
        self.subject = subject
        self.body = body
        self.attachments = attachments
        self.from_ = from_
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.headers = headers
        self.date = date
        self.encryption = encryption
        
    def to_dict(self):
        return {
            "subject": self.subject,
            "body": self.body,
            "attachments": self.attachments,
            "from": self.from_,
            "to": self.to,
            "cc": self.cc,
            "bcc": self.bcc,
            "headers": self.headers,
            "date": self.date,
            "encryption": {
                "flag": self.encryption.flag,
                "bodyUuid": self.encryption.bodyUuid,
                "attachmentUuid": self.encryption.attachmentUuid
            }
        }


# def get_email_body(message):
#     if message.is_multipart():
#         for part in message.walk():
#             content_type = part.get_content_type()
#             if content_type in ["text/plain", "text/html"]:
#                 return part.get_payload(decode=True).decode()
#     else:
#         return message.get_payload(decode=True).decode()

def get_email_body(message):
    def decode_part(part):
        charset = part.get_content_charset()
        payload = part.get_payload(decode=True)
        try:
            return payload.decode(charset or 'utf-8')
        except UnicodeDecodeError:
            return payload.decode(charset or 'utf-8', errors='replace')

    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type in ["text/plain", "text/html"]:
                return decode_part(part)
    else:
        return decode_part(message)

def fetch_emails(username, password, imap_url, limit=15):
    print("inside fetch emails", username, password, imap_url)
    # Connect to the server
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(username, password)
    mail.select('INBOX')

    status, messages = mail.search(None, 'ALL')
    print("status", status)
    messages = messages[0].split(b' ')

    email_objects = []
    id_c = 0
    for mail_id in messages[-limit:]:  # Fetch last 'limit' emails
        status, data = mail.fetch(mail_id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        subject = decode_header(email_message['Subject'])[0][0]
        subject = subject.decode() if isinstance(subject, bytes) else subject

        headers = {key: value for key, value in email_message.items()}
        from_ = headers.get("From")
        to = headers.get("To")
        cc = headers.get("Cc")
        bcc = headers.get("Bcc")
        date = headers.get("Date")
        # Handle encryption
        encryption = EncryptionInfo()
        for key, value in headers.items():
            if key == "X-Body-Encryption" and value.startswith("OTP"):
                encryption.flag = 1
                encryption.bodyUuid = value[18:]
            elif key == "X-Attachment-Encryption" and value.startswith("OTP"):
                encryption.flag = 1
                encryption.attachmentUuid = value[24:]
            elif key == "X-Body-Encryption" and value.startswith("AES"):
                encryption.flag = 2
            elif key == "X-Attachment-Encryption" and value.startswith("AES"):
                encryption.flag = 2

        body = get_email_body(email_message)
        attachments = []

        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is not None:
                    filename = part.get_filename()
                    if filename:
                        attachment_data = part.get_payload(decode=True)
                        attachments.append({
                            'filename': filename,
                            'data': base64.b64encode(attachment_data).decode()
                        })

        email_obj = EmailObject(subject, body, attachments, from_, to, cc, bcc, headers,date,encryption)
        email_obj.id = id_c
        id_c = id_c + 1
        email_objects.append(email_obj)
        print(email_obj)
        # [{
    print("here")
    mail.close()
    mail.logout()
    return email_objects

# fetch_emails("dastitwa@hotmail.com", "astitwa123", "imap-mail.outlook.com")
# fetch_emails("20cs3011@rgipt.ac.in", "nskd kizg vxba plqs", "imap.gmail.com")