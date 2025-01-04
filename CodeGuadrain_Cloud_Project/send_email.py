

# HORCRUX/CodeGuadrain_Cloud_Project/send_email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os
import markdown  # Import the markdown module
import re

load_dotenv()

email_address = os.getenv('EMAIL')
email_password = os.getenv('PASSWORD')  # Replace with your email password

# SMTP server configuration
smtp_server = "asmtp.bilkent.edu.tr"
smtp_port = 587  # STARTTLS Port

# Email details
subject = "Code Vulnerability Report"

def send_email(report_content, recipient_email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Check if the email matches the regex
    if not re.match(email_regex, recipient_email):
        return "Invalid email address"
    
    # Convert markdown to HTML
    html_body = markdown.markdown(report_content)

    # Create the email
    message = MIMEMultipart()
    message["From"] = "CodeGuardian <alper.mumcular@ug.bilkent.edu.tr>"
    message["To"] = recipient_email
    message["Subject"] = subject

    # Email body with markdown content converted to HTML
    body = f"""
    <html>
    <body>
        {html_body}
    </body>
    </html>
    """

    message.attach(MIMEText(body, "html"))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start TLS for security
        server.starttls()
        # Login to the email account
        server.login(email_address, email_password)
        # Send the email
        server.sendmail(email_address, recipient_email, message.as_string())
        print("Email sent successfully!")
