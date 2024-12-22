import random
from socket import *
import time
# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Bind the socket to an address and port
serverSocket.bind(('', 12000))

print("UDP Heartbeat Server is running...")

while True:
    # Generate a random number to simulate packet loss (30% loss)
    rand = random.randint(0, 10)

    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    
    # Simulate packet loss: if rand < 3 (30% chance), consider the packet lost
    if rand < 3:
        print(f"Packet from {address} lost.")
        continue  # Do not respond to this packet

    # Process the heartbeat message
    timestamp, sequence_number = message.decode().split()

    # Send back the time difference
    serverSocket.sendto(f"{time.time() - float(timestamp):.6f} {sequence_number}".encode(), address)


