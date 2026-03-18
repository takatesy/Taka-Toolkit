import os
import socket
import threading
import requests
import datetime
import subprocess
import re
from colorama import Fore, Style, init
from mac_vendor_lookup import MacLookup

init(autoreset=True)

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
    print("    [5] OSINT Profile Builder")
    print("    [6] Network Mapper")
    print("    [7] Exit\n")

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

def osint_search():
    clear()
    print("=== OSINT PROFILE BUILDER ===\n")
    username = input("Enter username to search: ")
    found = []
    lock = threading.Lock()

    sites = {
        "GitHub": "https://github.com/{}",
        "Twitter/X": "https://twitter.com/{}",
        "Instagram": "https://www.instagram.com/{}",
        "TikTok": "https://www.tiktok.com/@{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "YouTube": "https://www.youtube.com/@{}",
        "Twitch": "https://www.twitch.tv/{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "Tumblr": "https://{}.tumblr.com",
        "Flickr": "https://www.flickr.com/people/{}",
        "Vimeo": "https://vimeo.com/{}",
        "SoundCloud": "https://soundcloud.com/{}",
        "Spotify": "https://open.spotify.com/user/{}",
        "Medium": "https://medium.com/@{}",
        "DevTo": "https://dev.to/{}",
        "Hashnode": "https://hashnode.com/@{}",
        "Gitlab": "https://gitlab.com/{}",
        "Bitbucket": "https://bitbucket.org/{}",
        "HackerNews": "https://news.ycombinator.com/user?id={}",
        "ProductHunt": "https://www.producthunt.com/@{}",
        "Keybase": "https://keybase.io/{}",
        "Pastebin": "https://pastebin.com/u/{}",
        "HackerOne": "https://hackerone.com/{}",
        "BugCrowd": "https://bugcrowd.com/{}",
        "Steam": "https://steamcommunity.com/id/{}",
        "Roblox": "https://www.roblox.com/user.aspx?username={}",
        "Chess.com": "https://www.chess.com/member/{}",
        "Duolingo": "https://www.duolingo.com/profile/{}",
        "Replit": "https://replit.com/@{}",
        "Codecademy": "https://www.codecademy.com/profiles/{}",
    }

    print(f"\n{Fore.CYAN}Searching for username: {username}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Checking {len(sites)} sites...{Style.RESET_ALL}\n")

    def check_site(name, url_template):
        url = url_template.format(username)
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                with lock:
                    found.append((name, url))
                    print(f"{Fore.GREEN}  [FOUND] {name}: {url}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  [NOT FOUND] {name}{Style.RESET_ALL}")
        except:
            print(f"{Fore.YELLOW}  [ERROR] {name}{Style.RESET_ALL}")

    threads = []
    for name, url_template in sites.items():
        thread = threading.Thread(target=check_site, args=(name, url_template))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"osint_{username}_{timestamp}.txt"

    with open(report_name, "w") as f:
        f.write(f"OSINT Report for username: {username}\n")
        f.write(f"Generated: {timestamp}\n")
        f.write(f"{'='*50}\n\n")
        for name, url in found:
            f.write(f"[FOUND] {name}: {url}\n")

    print(f"\n{Fore.CYAN}Search complete.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Found {len(found)} profiles.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Report saved to: {report_name}{Style.RESET_ALL}")
    input("\nPress Enter to return to menu...")

def network_mapper():
    clear()
    print("=== NETWORK MAPPER ===\n")

    def get_local_ip():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip

    def get_mac(ip):
        try:
            output = subprocess.check_output(f"arp -a {ip}", shell=True).decode()
            mac = re.search(r"([0-9a-f]{2}[:-]){5}[0-9a-f]{2}", output, re.IGNORECASE)
            if mac:
                return mac.group()
        except:
            pass
        return "Unknown"

    def get_hostname(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"

    def get_vendor(mac):
        try:
            return MacLookup().lookup(mac)
        except:
            return "Unknown"

    def scan_host(ip, results, lock):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, 80))
            sock.close()

            if result == 0:
                mac = get_mac(ip)
                hostname = get_hostname(ip)
                vendor = get_vendor(mac)
                with lock:
                    results.append({"ip": ip, "mac": mac, "hostname": hostname, "vendor": vendor})
                    print(f"  {Fore.GREEN}[FOUND] {ip}{Style.RESET_ALL}")
            else:
                ping = subprocess.call(
                    f"ping -n 1 -w 500 {ip}",
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                if ping == 0:
                    mac = get_mac(ip)
                    hostname = get_hostname(ip)
                    vendor = get_vendor(mac)
                    with lock:
                        results.append({"ip": ip, "mac": mac, "hostname": hostname, "vendor": vendor})
                        print(f"  {Fore.GREEN}[FOUND] {ip}{Style.RESET_ALL}")
        except:
            pass

    local_ip = get_local_ip()
    base_ip = ".".join(local_ip.split(".")[:3])

    print(f"Your IP: {Fore.CYAN}{local_ip}{Style.RESET_ALL}")
    print(f"Scanning: {Fore.CYAN}{base_ip}.1 - {base_ip}.254{Style.RESET_ALL}\n")
    print("This will take 30-60 seconds...\n")

    results = []
    lock = threading.Lock()
    threads = []

    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        thread = threading.Thread(target=scan_host, args=(ip, results, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"\n{'='*60}")
    print(f"NETWORK MAP — {base_ip}.0/24")
    print(f"{'='*60}\n")

    for device in sorted(results, key=lambda x: int(x["ip"].split(".")[-1])):
        print(f"{Fore.CYAN}IP:{Style.RESET_ALL}       {device['ip']}")
        print(f"{Fore.CYAN}MAC:{Style.RESET_ALL}      {device['mac']}")
        print(f"{Fore.CYAN}Hostname:{Style.RESET_ALL} {device['hostname']}")
        print(f"{Fore.CYAN}Vendor:{Style.RESET_ALL}   {device['vendor']}")
        print(f"{'-'*40}")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report = f"netmap_{timestamp}.txt"

    with open(report, "w") as f:
        f.write(f"Network Map Report\n")
        f.write(f"Generated: {timestamp}\n")
        f.write(f"Network: {base_ip}.0/24\n")
        f.write(f"{'='*60}\n\n")
        for device in sorted(results, key=lambda x: int(x["ip"].split(".")[-1])):
            f.write(f"IP: {device['ip']} | MAC: {device['mac']} | Hostname: {device['hostname']} | Vendor: {device['vendor']}\n")

    print(f"\n{Fore.GREEN}Found {len(results)} devices.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Report saved to: {report}{Style.RESET_ALL}")
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
        osint_search()
    elif choice == "6":
        network_mapper()
    elif choice == "7":
        print("\n    Goodbye.\n")
        break
    else:
        print("\n    Invalid option.")
        input("    Press Enter to continue...")