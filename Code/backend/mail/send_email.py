from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Your email and password (consider using environment variables or a config file)
sender_email = "basushrabana16@gmail.com"
password = "Intern2324"  # Use a secure way to store your password

receiver_email = "sheshrabana1996@gmail.com"

msg = MIMEMultipart()

# Read the content of the text file
with open("text.txt", "r") as text_file:
    content = text_file.read()

# Attach the text file
file = MIMEText(content)
file.add_header("Content-Disposition", f"attachment; filename=text.txt")
msg.attach(file)

# Read and attach the image file (if available)
try:
    with open("image.png", "rb") as image_file:
        content = image_file.read()
        file = MIMEBase("application", "octet-stream")
        file.set_payload(content)
        encoders.encode_base64(file)
        file.add_header("Content-Disposition", "attachment; filename=image.png")
        msg.attach(file)
except FileNotFoundError:
    print("Image file 'image.png' not found.")

# Establish an SMTP connection
with smtplib.SMTP("localhost", 1025) as server:
    # Login to your email account (use your SMTP server and port)
    server.login(sender_email, password)

    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())

print("Email sent successfully.")