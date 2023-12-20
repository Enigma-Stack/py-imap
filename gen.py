import imaplib
import email

# Login credentials
username = 'dastitwa@hotmail.com'
password = 'astitwa123'

# Connect to the server
imap_url = 'imap-mail.outlook.com'
mail = imaplib.IMAP4_SSL(imap_url)

# Login
mail.login(username, password)

# Select the mailbox (INBOX in this case)
mail.select('inbox')

# Search for all emails in the inbox
result, data = mail.search(None, 'ALL')
print(result)

# Fetch the latest email
email_ids = data[0].split()
latest_email_id = email_ids[-1]

# Fetch the email by its ID
result, data = mail.fetch(latest_email_id, '(RFC822)')

# Parse the email content
raw_email = data[0][1]
parsed_email = email.message_from_bytes(raw_email)

# Print the subject
print("Subject:", parsed_email['Subject'])

# Close the connection
mail.close()
mail.logout()
