import os
import socket
import threading
import requests

def clear():
    os.system("cls")

def banner():
    print("""
'|''|''|'    /\\     |'' /    /\\    
    |       /  \\    |--<    /  \\   
    |      /----\\   |   \\  /----\\  
    |     /      \\  |    \\/      \\ 
    """)
    print("    @takatesy\n")
    print("    [1] Port Scanner")
    print("    [2] Banner Grabber")
    print("    [3] Directory Brute Forcer")
    print("    [4] Password Brute Forcer")
    print("    [5] Exit\n")

def port_scanner():
    clear()
    print("=== PORT SCANNER ===\n")
    target = input("Enter target IP or website: ")
    start_port = int(input("Start port (e.g. 1): "))
    end_port = int(input("End port (e.g. 1024): "))
    
    open_ports = []
    lock = threading.Lock()

    print(f"\nScanning {target}...\n")

    def scan_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        if result == 0:
            with lock:
                open_ports.append(port)
                print(f"  [OPEN] Port {port}")
        sock.close()

    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    print(f"\nScan complete. Open ports: {sorted(open_ports)}")
    input("\nPress Enter to return to menu...")

def banner_grabber():
    clear()
    print("=== BANNER GRABBER ===\n")
    target = input("Enter target IP or website: ")
    port = int(input("Enter port: "))

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((target, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode(errors="ignore")
        print(f"\nBanner from {target}:{port}\n")
        print(banner)
        sock.close()
    except Exception as e:
        print(f"Could not grab banner: {e}")

    input("\nPress Enter to return to menu...")

def dir_bruteforce():
    clear()
    print("=== DIRECTORY BRUTE FORCER ===\n")
    target = input("Enter target URL (e.g. http://example.com): ")
    wordlist = input("Enter wordlist path: ")

    found = []
    lock = threading.Lock()

    with open(wordlist, "r") as f:
        words = f.read().splitlines()

    print(f"\nLoaded {len(words)} words")
    print(f"Bruteforcing {target}...\n")

    def check_dir(word):
        url = f"{target}/{word}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                with lock:
                    found.append(url)
                    print(f"  [FOUND] {url}")
            elif response.status_code == 403:
                print(f"  [FORBIDDEN] {url}")
            else:
                print(f"  [{response.status_code}] {url}")
        except:
            pass

    threads = []
    for word in words:
        thread = threading.Thread(target=check_dir, args=(word,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    print(f"\nScan complete. Found {len(found)} directories.")
    input("\nPress Enter to return to menu...")

def pass_bruteforce():
    clear()
    print("=== PASSWORD BRUTE FORCER ===\n")
    target = input("Enter login URL: ")
    username = input("Enter username to attack: ")
    wordlist = input("Enter password wordlist path: ")
    success_text = input("Enter text that appears on FAILED login: ")

    found = False

    with open(wordlist, "r") as f:
        passwords = f.read().splitlines()

    print(f"\nLoaded {len(passwords)} passwords")
    print(f"Attacking {target} with username: {username}\n")

    def try_password(password):
        nonlocal found
        try:
            data = {"username": username, "password": password}
            response = requests.post(target, data=data, timeout=3)
            if success_text not in response.text:
                found = True
                print(f"\n  [SUCCESS] Password found: {password}")
            else:
                print(f"  [FAIL] {password}")
        except Exception as e:
            print(f"  [ERROR] {password}: {e}")

    for password in passwords:
        if found:
            break
        try_password(password)

    if not found:
        print("\nPassword not found in wordlist.")

    input("\nPress Enter to return to menu...")

# --- MAIN LOOP ---
while True:
    clear()
    banner()
    choice = input("    Select tool: ")

    if choice == "1":
        port_scanner()
    elif choice == "2":
        banner_grabber()
    elif choice == "3":
        dir_bruteforce()
    elif choice == "4":
        pass_bruteforce()
    elif choice == "5":
        print("\n    Goodbye.\n")
        break
    else:
        print("\n    Invalid option.")
        input("    Press Enter to continue...")