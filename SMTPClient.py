from socket import *
import ssl
import base64
from email.base64mime import body_encode as encode_base64
import os
from dotenv import load_dotenv, find_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
envpassword = os.getenv("PASSWORD")

def auth_plain(sender_email, password):
    return "\0%s\0%s" % (sender_email, password)

# Create a multipart message
msg = MIMEMultipart()

# Set the email parameters
msg['From'] = 'yuvalsmith1@gmail.com'
msg['To'] = 'yuval.g.smith@gmail.com'
msg['Subject'] = 'Sent with SMTPClient.py'

# Attach the body of the email
body = 'This email was sent with SMTPClient.py!\r\nWe appreciate you using this tool!'
msg.attach(MIMEText(body, 'plain'))

# Open the file in bynary mode
# Open the file in bynary mode
with open('cat_with_bear.jpg', 'rb') as binary_file:
    mime = MIMEBase('image', 'jpg', filename='cat_with_bear.jpg')
    # Add header
    mime.add_header('Content-Disposition', 'attachment', filename='cat_with_bear.jpg')
    # Read the file content and encode into base64
    mime.set_payload(binary_file.read())
    encoders.encode_base64(mime)

    # Add the image to the email
    msg.attach(mime)

# Convert the multipart message to a string
msg_str = msg.as_string()

# Define the SMTP server
mailserver = "smtp.gmail.com"

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 587))

recv = clientSocket.recv(1024)
print(recv)

heloCommand = 'EHLO yuval\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
print(recv1)

# Start TLS encryption
starttlsCommand = 'STARTTLS\r\n'
clientSocket.send(starttlsCommand.encode())
recv1 = clientSocket.recv(1024)
print(recv1)

# Create a default SSL context
context = ssl.create_default_context()

# Wrap the socket in the SSL context
ssl_clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

# Now you can continue with the AUTH command
authCommand = 'AUTH PLAIN\r\n'
ssl_clientSocket.send(authCommand.encode())
recv1 = ssl_clientSocket.recv(1024)
print(recv1)

# Wait for the server's response before sending the username and password
if recv1.startswith(b'334'):
    username = 'yuvalsmith1@gmail.com'
    password = envpassword
    auth_string = '\0{0}\0{1}'.format(username, password)
    auth_bytes = base64.b64encode(auth_string.encode())
    ssl_clientSocket.send(auth_bytes + b'\r\n')
    recv1 = ssl_clientSocket.recv(1024)
    print(recv1)

ssl_clientSocket.send(auth_bytes + b'\r\n')
recv1 = ssl_clientSocket.recv(1024)
print("Authentication completed")

# Continue with the rest of the commands
mailFrom = "MAIL FROM: <yuvalsmith1@gmail.com>\r\n"
ssl_clientSocket.send(mailFrom.encode())
recv2 = ssl_clientSocket.recv(1024)
print("MAIL FROM command sent")

rcptTo = "RCPT TO: <yuval.g.smith@gmail.com>\r\n"
ssl_clientSocket.send(rcptTo.encode())
recv3 = ssl_clientSocket.recv(1024)
print("RCPT TO command sent")

data = "DATA\r\n"
ssl_clientSocket.send(data.encode())
recv4 = ssl_clientSocket.recv(1024)
print("DATA command sent")

msg_str += '\r\n.\r\n'
ssl_clientSocket.send(msg_str.encode())
print("Message sent")

recv5 = ssl_clientSocket.recv(1024)
print(recv5)

quitCommand = "QUIT\r\n"
ssl_clientSocket.send(quitCommand.encode())
recv6 = ssl_clientSocket.recv(1024)
print(recv6)

ssl_clientSocket.close()