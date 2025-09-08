import smtplib

sender = "sender@example.com"
receiver = "receiver@example.com"
message = """\
Subject: Test Email

This is a test email from Python.
"""

try:
    with smtplib.SMTP("localhost", 1025) as server:
        server.sendmail(sender, receiver, message)
        print("Email sent successfully")
except Exception as e:
    print("SMTP error:", e)
