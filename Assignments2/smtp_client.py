import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender, password, recipient, subject, message):
    """Send an email using Gmail's SMTP server."""
    
    # create the email container
    email = MIMEMultipart()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = subject

    # attach body text
    email.attach(MIMEText(message, "plain"))

    try:
        # connect to Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()  # switch to secure connection
            smtp.login(sender, password)
            smtp.sendmail(sender, recipient, email.as_string())
        print("✅ Mail delivered successfully!")

    except Exception as e:
        print("❌ Something went wrong:", e)


if __name__ == "__main__":
    # configure your details here
    my_email = "your_email@gmail.com"
    app_pass = "your_16_char_app_password"
    to_email = "receiver_email@gmail.com"

    subject_line = "Python SMTP Demo"
    body_text = "Hi! This is a test email sent via Python with Gmail SMTP."

    send_email(my_email, app_pass, to_email, subject_line, body_text)
