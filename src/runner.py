from scapy.all import IP, TCP, sr1
from netaddr import IPNetwork
from time import perf_counter

import sys
results = {}



def scan_network(network):
    # Define the port to scan
    target_port = 80
    
    # Create an IP network object using netaddr
    ip_network = IPNetwork(network)
    
    # Scan each host in the provided network
    for ip in ip_network:
        print(f"Scanning {ip}...")
        # Create a packet with IP and TCP layers
        packet = IP(dst=str(ip)) / TCP(dport=target_port, flags='S')
        
        # Send the packet and wait for a response
        response = sr1(packet, timeout=2, verbose=0)
        
        is_open = bool(response and response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12)
        # Check if the response has the TCP layer with SYN-ACK flags
        if is_open:  # SYN-ACK response
            results[ip] = True
        
    return results

if __name__ == "__main__":
    t1_start = perf_counter() 
    if len(sys.argv) != 2:
        print("Usage: python runner.py <network>")
        sys.exit(1)

    network = sys.argv[1]
    results = scan_network(network)
    t1_stop = perf_counter()
    print(results)
    print(f"Took (seconds): {t1_stop-t1_start}")

