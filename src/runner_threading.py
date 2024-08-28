from scapy.all import IP, TCP, sr1
from netaddr import IPNetwork
import sys
import threading
from time import perf_counter

# Define a semaphore to limit the number of concurrent threads
MAX_THREADS = 100
semaphore = threading.Semaphore(MAX_THREADS)

# Shared dictionary to store scan results
results = {}
# Lock to control access to the results dictionary
lock = threading.Lock()

def scan_ip(ip, target_port):
    """Scan a single IP for the specified port."""
    with semaphore:  # Control the number of concurrent threads
        packet = IP(dst=ip) / TCP(dport=target_port, flags='S')
        response = sr1(packet, timeout=1, verbose=0)

        # Determine if the port is open
        is_open = bool(response and response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12)

        # Safely update the shared results dictionary
        if is_open:
            with lock:
                results[ip] = is_open

def scan_network(network):
    """Scan the entire network for the specified port."""
    target_port = 80
    ip_network = IPNetwork(network)
    threads = []

    for ip in ip_network:
        ip_str = str(ip)
        # Create a new thread for each IP scan
        thread = threading.Thread(target=scan_ip, args=(ip_str, target_port))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Print the final results dictionary
    print("\nScan Results:")
    for ip, is_open in results.items():
        print(f"{ip}: {'Open' if is_open else 'Closed'}")

if __name__ == "__main__":
    t1_start = perf_counter() 
    if len(sys.argv) != 2:
        print("Usage: python scan.py <network>")
        sys.exit(1)

    network = sys.argv[1]
    scan_network(network)
    t1_stop = perf_counter()
    print(f"Took (seconds): {t1_stop-t1_start}")
