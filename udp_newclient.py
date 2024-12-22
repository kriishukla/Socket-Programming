import time
import socket
import sys

server_name = 'localhost'  
server_port = 12000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
timer = 1
client_socket.settimeout(timer) 

mir = 0  
hbc = 0  
successful_responses = 0  
rtts = []  

while True:
    hbc += 1
    timestamp = time.time()
    message = f"{timestamp} {hbc}"

    try:
        client_socket.sendto(message.encode(), (server_name, server_port))

        start_time = time.time()

        rsp, sva = client_socket.recvfrom(1024)

        end_time = time.time()
        
        rtt = end_time - start_time
        rtts.append(rtt)

        td, seqn = rsp.decode().split()
        sys.stdout.write(f"Reply from {sva}: Time difference: {td} seconds, Sequence: {seqn}\n")
        
        mir = 0
        successful_responses += 1

    except socket.timeout:
        sys.stdout.write("Request timed out\n")
        mir += 1

        if mir >= 3:
            sys.stdout.write(f"Server is down after {hbc} heartbeats sent.\n")
            break

    time.sleep(1)

client_socket.close()

total_sent = hbc
total_timeouts = mir
total_received = successful_responses
failure_rate = ((total_sent-total_received) / total_sent) * 100 if total_sent > 0 else 0

if successful_responses > 0:
    avg_rtt = sum(rtts) / successful_responses
    min_rtt = min(rtts)
    max_rtt = max(rtts)
else:
    avg_rtt = min_rtt = max_rtt = None

sys.stdout.write("\n--- Statistics ---\n")
sys.stdout.write(f"Total Heartbeats Sent: {total_sent}\n")
sys.stdout.write(f"Total Responses Received: {total_received}\n")
sys.stdout.write(f"Total Timeouts: {total_timeouts}\n")
sys.stdout.write(f"Percentage of Failed Responses: {failure_rate:.2f}%\n")

if successful_responses > 0:
    sys.stdout.write(f"Average RTT for Successful Responses: {avg_rtt:.6f} seconds\n")
    sys.stdout.write(f"Minimum RTT for Successful Responses: {min_rtt:.6f} seconds\n")
    sys.stdout.write(f"Maximum RTT for Successful Responses: {max_rtt:.6f} seconds\n")
else:
    sys.stdout.write("No successful responses received; RTT statistics not available.\n")
