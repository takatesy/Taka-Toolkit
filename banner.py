import socket
target = input("Enter Target IP or Website: ")
port = int(input("Enter port to grab banner from: "))

try: 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((target, port))

    sock.send(b"Head / HTTP/1.0\r\n\r\n")

    banner = sock.recv(1024).decode(errors="ignore")

    print(f"\nBanner grabbed from {target}:{port}\n")
    print(banner)

    sock.close()

except Exception as e:
    print(f"Coult not grab banner: {e}")