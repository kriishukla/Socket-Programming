import time
import socket

name = 'localhost'  
prt = 12000
cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
timer =1
cs.settimeout(timer)  

arr = [] 
lost = 0

i = 1
while i <= 10:
    msg = f"Ping {i} {time.time()}"
    try:
        start_time = time.time()

        cs.sendto(msg.encode(), (name, prt))

        response, server_address = cs.recvfrom(1024)

        end_time = time.time()

        arr.append(end_time - start_time)

        print(f"Reply from {server_address}: {response.decode()}")
        print(f"RTT: {end_time - start_time:.6f} seconds")

    except socket.timeout:
        print(f"Request timed out")
        lost += 1

    i += 1

cs.close()

try:
    print(f"\nMinimum RTT: {min(arr):.6f} seconds")
except ValueError:
    print("\nMinimum RTT: No packets received")

try:
    print(f"Maximum RTT: {max(arr):.6f} seconds")
except ValueError:
    print("Maximum RTT: No packets received")

try:
    print(f"Average RTT: {sum(arr) / len(arr):.6f} seconds")
except ZeroDivisionError:
    print("Average RTT: No packets received")

print(f"Packet Loss Rate: {lost * 10}%")