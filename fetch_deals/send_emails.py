import smtplib
from email.mime.text import MIMEText
FROM_EMAIL = "ajaygoli1701@gmail.com"
APP_PASSWORD = "tdal xdyp brhz jjer"

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.send_message(msg)
            print(f"✅ Email sent to {to}")
    except Exception as e:
        print(f"❌ Failed to send email to {to}: {e}")