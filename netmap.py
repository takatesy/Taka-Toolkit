import socket
import threading
import subprocess
import re
from mac_vendor_lookup import MacLookup
import datetime

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
                results.append({
                    "ip": ip,
                    "mac": mac,
                    "hostname": hostname,
                    "vendor": vendor
                })
                print(f"  [FOUND] {ip}")
        else:
            # Try ping
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
                    results.append({
                        "ip": ip,
                        "mac": mac,
                        "hostname": hostname,
                        "vendor": vendor
                    })
                    print(f"  [FOUND] {ip}")
    except:
        pass

local_ip = get_local_ip()
base_ip = ".".join(local_ip.split(".")[:3])

print("=== TAKA NETWORK MAPPER ===\n")
print(f"Your IP: {local_ip}")
print(f"Scanning network: {base_ip}.1 - {base_ip}.254\n")
print("Scanning...\n")

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
    print(f"IP:       {device['ip']}")
    print(f"MAC:      {device['mac']}")
    print(f"Hostname: {device['hostname']}")
    print(f"Vendor:   {device['vendor']}")
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

print(f"\nFound {len(results)} devices.")
print(f"Report saved to: {report}")