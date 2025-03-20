import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from config import SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

def send_email_with_screenshot(screenshot_path):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "WhatsApp Web QR Code Detected"

    body = "The WhatsApp Web script encountered the QR code page. Please find the screenshot attached."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(screenshot_path, 'rb') as img_file:
            img = MIMEImage(img_file.read(), name=os.path.basename(screenshot_path))
            msg.attach(img)
    except FileNotFoundError:
        print(f"Error: Screenshot file not found at {screenshot_path}")
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
