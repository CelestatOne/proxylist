import subprocess
import sys

# Функция для установки зависимостей
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Проверка и установка зависимостей
try:
    import requests
except ImportError:
    print("requests not found, installing...")
    install("requests")

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup not found, installing...")
    install("beautifulsoup4")

try:
    import requests
    from bs4 import BeautifulSoup
    from random import choice
except ImportError as e:
    print(f"Failed to import required modules: {e}")
    sys.exit(1)

def get_proxies():
    url = "https://free-proxy-list.net/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch proxies from {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    proxies = [i for i in list(map(lambda x: x[0] + ':' + x[1] if x[1].isdigit() and len(x[0]) > 6 else "", list(zip(map(lambda x: x.text, soup.find_all("td")[::8]), map(lambda x: x.text, soup.find_all("td")[1::8]))))) if i and i[4] != '-']
    return proxies

def check_proxy(proxy):
    try:
        print(f"Testing proxy: {proxy}")
        response = requests.get("https://www.olx.ua", timeout=5, proxies={"https": proxy})
        if response.status_code == 200:
            print(f"Proxy {proxy} works!")
            return True
    except:
        print(f"Proxy {proxy} failed.")
        return False

def find_working_proxies(proxies, num_proxies):
    working_proxies = []
    while len(working_proxies) < num_proxies and proxies:
        proxy = choice(proxies)
        if check_proxy(proxy):
            working_proxies.append(proxy)
        proxies.remove(proxy)
    return working_proxies

def save_proxies(proxies, filename):
    with open(filename, 'w') as file:
        for proxy in proxies:
            file.write(f"https://{proxy}\n")

def main():
    print("Fetching proxies...")
    proxies = get_proxies()
    
    if not proxies:
        user_proxy = input("Enter proxy URL (or leave blank to not use proxy): ").strip()
        if user_proxy:
            proxies = [user_proxy]
        else:
            print("No proxies fetched. Exiting.")
            return
    
    print(f"Fetched {len(proxies)} proxies.")
    
    num_proxies = int(input("Enter the number of working proxies to find: "))
    print(f"Finding {num_proxies} working proxies...")
    
    working_proxies = find_working_proxies(proxies, num_proxies)
    print(f"Found {len(working_proxies)} working proxies.")
    
    save_proxies(working_proxies, 'working_proxies.txt')
    print("Working proxies saved to 'working_proxies.txt'.")

if __name__ == "__main__":
    main()
