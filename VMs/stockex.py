import imaplib
import email
import os
import subprocess
from datetime import datetime, timedelta
import stat

# Email configuration
EMAIL = 'stockexchangecpsmyra@gmail.com'
PASSWORD = 'qskr sbxv ubnh bink'
SERVER = 'imap.gmail.com'

# Get today's date and subtract 1 day (24 hours)
yesterday = (datetime.now() - timedelta(1)).strftime("%d-%b-%Y")

# List of phishing keywords to simulate "tempting" emails
phishing_keywords = ["free", "get salary", "urgent", "reward", "congratulations", "important"]

# Function to check if email is phishing-like
def is_phishing_email(subject, body):
    subject = subject.lower()
    body = body.lower()
    for keyword in phishing_keywords:
        if keyword in subject or keyword in body:
            return True
    return False

# Function to give executable permissions and execute the file
def execute_file(file_path):
    # Give the file executable permissions
    os.chmod(file_path, stat.S_IRWXU)  # Owner can read, write, and execute

    # Determine the file extension and execute the file accordingly
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.py':
        # Execute Python script
        print(f"Executing Python file: {file_path}")
        subprocess.call(['sudo', 'python3', file_path])
    elif file_extension == '.sh':
        # Execute Shell script
        print(f"Executing Shell script: {file_path}")
        subprocess.call(['sudo', 'bash', file_path])
    elif file_extension in ['.exe', '.bat']:
        # Execute Windows executable or batch script
        print(f"Executing Windows executable or batch script: {file_path}")
        subprocess.call([file_path])
    else:
        # For other file types, attempt to open with the system's default program
        print(f"Attempting to open file with the system's default program: {file_path}")
        subprocess.call(['sudo', 'xdg-open', file_path])

try:
    # Connect to the email server
    print("Connecting to email server...")
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    print("Login successful!")

    # Select inbox
    print("Selecting inbox...")
    mail.select('inbox')

    # Search for emails from the last 24 hours
    print(f"Searching for emails since {yesterday}...")
    status, messages = mail.search(None, f'(SINCE "{yesterday}")')
    email_ids = messages[0].split()

    if len(email_ids) == 0:
        print("No emails found from the last 24 hours.")
    else:
        print(f"Found {len(email_ids)} email(s) from the last 24 hours.")

    for e_id in email_ids:
        # Fetch the email by its ID
        print(f"Reading email with ID: {e_id.decode()}")
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        # Get the email subject
        email_subject = email.header.decode_header(msg['Subject'])[0][0]
        if isinstance(email_subject, bytes):
            email_subject = email_subject.decode()
        print(f"Email Subject: {email_subject}")

        # Get the sender email address
        email_from = email.utils.parseaddr(msg['From'])[1]
        print(f"Email From: {email_from}")

        # Get the email body
        email_body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    email_body += part.get_payload(decode=True).decode()
        else:
            email_body = msg.get_payload(decode=True).decode()

        # Check if the email looks like phishing
        if is_phishing_email(email_subject, email_body):
            print(f"Email with subject '{email_subject}' appears to be phishing, checking for attachments...")

            # Process the email content and check for attachments
            for part in msg.walk():
                # Skip if it's a multipart container
                if part.get_content_maintype() == 'multipart':
                    continue

                # Check for attachments
                if part.get('Content-Disposition') is None:
                    continue

                # Save the attachment
                file_name = part.get_filename()
                if file_name:
                    file_path = os.path.join('/home/alpha/Downloads', file_name)
                    with open(file_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Attachment {file_name} downloaded to {file_path}")

                    # Execute the downloaded file with elevated permissions
                    execute_file(file_path)
        else:
            print(f"Email with subject '{email_subject}' does not seem like phishing. Skipping...")

    print("All emails from the last 24 hours processed.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Logout from the mail server
    print("Logging out from the email server...")
    mail.logout()
    print("Logged out successfully.")
	
	
-----------------------------------------
stockex VM - crontab disabled
