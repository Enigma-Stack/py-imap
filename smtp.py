import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

port = 587
server = 'smtp.gmail.com'
logger = 'rajaryaman666@gmail.com'
passw = 'nduo ixui crqf hanq'
sender = 'rajaryaman666@gmail.com'
receiver = '20cs3014@rgipt.ac.in'
msg = MIMEMultipart("alternative")

file_paths = [r'C:\Users\aks02\OneDrive\Pictures\Screenshots\Screenshot 2023-06-01 200934.png']  # Replace with actual file paths

# Function to add attachments to the email
def attach_files(file_list):
    for file_path in file_list:
        attachment = open(file_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {file_path}')
        msg.attach(part)

msg['From'] = 'rajaryaman666@gmail.com'
msg['To'] = '20cs3014@rgipt.ac.in'
msg['Subject'] = 'simple email in python'
message = 'Test'
part1 = MIMEText(message,"plain")
msg.attach(part1)
context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    server.login(logger,passw)
    server.sendmail(sender,receiver,msg.as_string())
print('Sent')