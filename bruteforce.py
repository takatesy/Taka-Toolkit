import requests
import threading

target = input("Enter target URL (e.g. http://example.com): ")
wordlist = input("Enter wordlist path: ")

found = []
lock = threading.Lock()

with open(wordlist, "r") as f:
    words = f.read().splitlines()

print(f"\nBruteforcing {target}...\n")

def check_dir(word):
    print(f"Checking {word}")
    url = f"{target}/{word}"
    try:

        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            with lock:
                found.append(url)
                print(f"[FOUND] {url}")
        elif response.status_code == 403:
            print(f"[FORBIDDEN] {url}")
        else:
            print(f"[{response.status_code}] {url}")
    except Exception as e:
        print(f"[ERROR] {word}: {e}")


threads = []

for word in words:
    thread = threading.Thread(target=check_dir, args=(word,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f"\nScan complete. Found {len(found)} directories.")