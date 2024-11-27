import socket
import threading
import queue

# Creates a queue for messages and a list for clients
messages = queue.Queue()
clients = []

# Creates a UDP socket server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9876))

# This function listens to incoming messages and puts them in the queue.
def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

# This function broadcasts the messages to all clients.
def broadcast():
    while True:
        while not messages.empty(): # If there are messages in the queue, it will broadcast them.
            message, addr = messages.get()
            print(message.decode())
            if addr not in clients: # If the client is new, it will add it to the list.
                clients.append(addr)
            for client in clients: # Sends the message to all clients
                try:
                    server.sendto(message, client)
                except:
                    clients.remove(client)

# Create the threads
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

# Start the threads
t1.start()
t2.start()
print("Server started.")

# Join the threads
t1.join()
t2.join()

# Close the server
server.close()