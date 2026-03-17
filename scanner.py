import socket
import threading


target = input("Enter target IP or website: ")
open_ports = []
lock = threading.Lock()


print(f"\nScanning {target}...\n")

def scan_port(port):
    sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target,port))

    if result == 0:
        open_ports.append(port)
        print(f"Port {port}: OPEN")
    sock.close()

threads = []

for port in range (1,1025):
    thread = threading.Thread(target=scan_port, args=(port,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("\nScan Complete.")
print(f"Open ports found: {sorted(open_ports)}")
