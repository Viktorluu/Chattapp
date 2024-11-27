import socket
import threading
import random

# Creates a UDP socket client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Binds the client to a random port
client.bind(("localhost", random.randint(8000,9000)))

# Asks for a nickname
name = input("Nickname: ")

# This function listens to incoming messages and prints them.
def receive() -> None:
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except socket.error:
            break

# Creates a thread for the receive function
t = threading.Thread(target=receive)
t.start()

# Sends a message to the server with the nickname
client.sendto(f"Welcome to the chat {name}!".encode(), ("localhost", 9876))

# This loop sends messages to the server
try:
    while True:
        message = input("")
        if message == "!quit":
            client.sendto(f"{name} has left the chat.".encode(), ("localhost", 9876))
            break
        else:
            client.sendto(f"{name}: {message}".encode(), ("localhost", 9876))

# If the user closes the client, it will close the client and join the thread.
finally:
    client.close()
    t.join()

