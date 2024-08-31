import requests
from bs4 import BeautifulSoup
import queue
import threading

q = queue.Queue()
valid_proxies = []

with open("valid_proxies.txt", "r") as f:
    proxies = f.read().split("\n")
    # print(proxies)
    for p in proxies:
        # print(p)
        q.put(p)

lock = threading.Lock()

def check_proxy(proxy):
    try:
        res = requests.get('http://ipinfo.io/json', proxies={"http": proxy, "https": proxy}, timeout=5)
        if res.status_code == 200:
            with lock:
                valid_proxies.append(proxy)
                print(proxy)
    except Exception as e:
        pass
def check_proxies():
    threads = []
    while not q.empty():
        proxy = q.get()
        thread = threading.Thread(target=check_proxy, args=(proxy,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

check_proxies()
