import requests
import threading
from colorama import Fore, Style, init
import datetime

init(autoreset=True)

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
                print(f"{Fore.GREEN}[FOUND] {name}: {url}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[NOT FOUND] {name}{Style.RESET_ALL}")
    except:
        print(f"{Fore.YELLOW}[ERROR] {name}{Style.RESET_ALL}")

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
    f.write(f"={'='*50}\n\n")
    for name, url in found:
        f.write(f"[FOUND] {name}: {url}\n")

print(f"\n{Fore.CYAN}Search complete.{Style.RESET_ALL}")
print(f"{Fore.GREEN}Found {len(found)} profiles.{Style.RESET_ALL}")
print(f"{Fore.CYAN}Report saved to: {report_name}{Style.RESET_ALL}")