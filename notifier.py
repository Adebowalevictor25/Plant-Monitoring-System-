# notifier.py
# Handles notifications for the Plant Monitoring System.

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN

# Telegram notifications
def send_telegram_notification(chat_id, message):
    """
    Sends a notification via Telegram.
    """
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=chat_id, text=message)
        print(f"Telegram notification sent to {chat_id}: {message}")
    except Exception as e:
        print(f"Error sending Telegram notification: {e}")

# Email notifications
def send_email_notification(to_email, subject, message):
    """
    Sends a notification via Email.
    """
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your-email@gmail.com"
        sender_password = "your-email-password"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())

        print(f"Email notification sent to {to_email}: {subject}")
    except Exception as e:
        print(f"Error sending email notification: {e}")

# Example notifications
if __name__ == "__main__":
    # Telegram Example
    chat_id = "123456789"
    send_telegram_notification(chat_id, "Test notification from Plant Monitoring System.")

    # Email Example
    recipient_email = "recipient@example.com"
    send_email_notification(
        recipient_email,
        "Plant Monitoring System Alert",
        "Your plants need watering!"
    )