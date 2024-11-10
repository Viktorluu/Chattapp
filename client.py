import socket
import threading
import random

# Create a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Create a bind to a random port between 8000-9000
client.bind(("localhost", random.randint(8000,9000)))

# Asks for userinput nickname
name = input("Nickname: ")

# A thread that listens to incoming messages from the server.
# When a message is received, it prints it out.
def receive() -> None:
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

# Sends a message to client about who joined.
client.sendto(f"SIGNUP_TAG:{name}".encode(), ("localhost", 9876))

# A loop that asks for a message. If the message is "!quit" the program exits.
# Else it sends a message to the server with nickname + the message (on port 9999)
while True:
    message = input("")
    if message == "!quit":
        exit()
    else:
        client.sendto(f"{name}: {message}".encode(), ("localhost", 9876))