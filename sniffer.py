from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
import datetime
import os

log_file = "packets.log"

def process_packet(packet):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        
        if TCP in packet:
            sport = packet[TCP].sport
            dport = packet[TCP].dport
            line = f"[{timestamp}] [TCP] {src}:{sport} -> {dst}:{dport}"
            
            if Raw in packet:
                payload = packet[Raw].load.decode(errors="ignore")
                if "HTTP" in payload or "GET" in payload or "POST" in payload:
                    line += f"\n  [HTTP] {payload[:200]}"
            
        elif UDP in packet:
            sport = packet[UDP].sport
            dport = packet[UDP].dport
            line = f"[{timestamp}] [UDP] {src}:{sport} -> {dst}:{dport}"
            
        elif ICMP in packet:
            line = f"[{timestamp}] [ICMP] {src} -> {dst}"
            
        else:
            line = f"[{timestamp}] [IP] {src} -> {dst}"
        
        print(line)
        
        with open(log_file, "a") as f:
            f.write(line + "\n")

print("=== TAKA PACKET SNIFFER ===")
print(f"Logging to {log_file}")
print("Press CTRL+C to stop\n")

sniff(prn=process_packet, store=False)