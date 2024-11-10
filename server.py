import socket
import threading
import queue

# Stores messages in a queue. FIFO queue.
# an empty list is created to store clients.
messages = queue.Queue()
clients = []

# Creates an UDP socket and binds it to localhost port 9876
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9876))

# This function listens to incoming messages and puts them in messages. 
def receive() -> None:
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

# This function listens to the new messages and broadcast them to all clients.
def broadcast() -> None:
    while True:
        while not messages.empty(): # is true if there are any messages in queue.
            message, addr = messages.get()
            print(message.decode())
            if addr not in clients: # If address (user) is not in clients, adds client.
                clients.append(addr)
            for client in clients: # This loop checks if a client has a signuptag. If it's new, sends a "joined!" message
                try:
                    if message.decode().startswith("SIGNUP_TAG:"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} joined!".encode(), client)
                    else: # Sends the message
                        server.sendto(message, client)
                except:
                    clients.remove(client)

# Creates the threads
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

# Start the threads
t1.start()
t2.start()
                    