from socket import *
import ssl
import base64
from email.base64mime import body_encode as encode_base64

def auth_plain(sender_email, password):
    return "\0%s\0%s" % (sender_email, password)

msg = "Subject: Sent with SMTPClient.py\r\n\r\nThis email was sent with SMTPClient.py!\r\nWe appreciate you using this tool!"
endmsg = "\r\n.\r\n"
mailserver = 'smtp.gmail.com'

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
    password = 'ivcwqvbjunbdlwjy'
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

ssl_clientSocket.send(msg.encode())
print("Message sent")
ssl_clientSocket.send(endmsg.encode())
recv5 = ssl_clientSocket.recv(1024)
print(recv5)

quitCommand = "QUIT\r\n"
ssl_clientSocket.send(quitCommand.encode())
recv6 = ssl_clientSocket.recv(1024)
print(recv6)

ssl_clientSocket.close()