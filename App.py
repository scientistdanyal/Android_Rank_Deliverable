import logging
import requests
import pyodbc
import time
import os
import json
from bs4 import BeautifulSoup

# Create the directory if it doesn't exist
log_directory = "c:\\tnlog\\"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
log_date = time.strftime("%m-%d-%Y")
log_file_path = os.path.join(log_directory, f"{log_date}.ARSP")
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s: %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')

# Read config file
config = json.load(open('config.json'))

# Get proxies list from config
proxies_list = config.get('proxies', [])

# Function to log HTTP request details
def log_http_request(method, url):
    logging.info(f"HTTP {method} request to URL: {url}")

# Function to log SQL queries
def log_sql_query(sql_query):
    logging.info(f"SQL Query: {sql_query}")

# Function to log key events
def log_event(event):
    logging.info(event)

# Function to check if proxy is working
def check_proxy(proxy):
    try:
        response = requests.get("https://www.example.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"Proxy {proxy} failed: {e}")
        return False

# Function to get a working proxy from the list
def get_working_proxy(proxies_list):
    for proxy in proxies_list:
        if check_proxy(proxy):
            print(f"Using proxy: {proxy}")
            return proxy
    print("No working proxies found.")
    return None

def All_developers():
    conn = pyodbc.connect(json.load(open('config.json'))['connectionString'])
    cursor = conn.cursor()
    cursor.execute("SELECT dev_id FROM Developers")
    developers = [row[0] for row in cursor.fetchall()]
    return developers

def save_application(data):
    try:
        conn = pyodbc.connect(json.load(open('config.json'))['connectionString'])
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Applications WHERE package_name = ?", data.get('ID', None))
        count = cursor.fetchone()[0]
        if count > 0:
            sql_query = '''
                UPDATE Applications
                SET dev_id = ?,
                    title = ?,
                    category = ?,
                    price = ?,
                    total_rating = ?,
                    growth_30 = ?,
                    growth_60 = ?,
                    average_rating = ?,
                    installs_achieved = ?,
                    installs_estimated = ?,
                    star_5 = ?,
                    star_4 = ?,
                    star_3 = ?,
                    star_2 = ?,
                    star_1 = ?,
                    rank=?
                WHERE package_name = ?
            '''
        else:
            sql_query = '''
                INSERT INTO Applications ( dev_id, title, category, price, total_rating, growth_30, growth_60, average_rating, installs_achieved,installs_estimated,star_5,star_4,star_3,star_2,star_1,rank,package_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?)
            '''
        values = (
            data.get('Developer:', None),
            data.get('Title:', None),
            data.get('Category:', None),
            data.get('Price:', None),
            data.get('Total ratings:', None),
            data.get('Growth (30 days):', None),
            data.get('Growth (60 days):', None),
            data.get('Average rating:', None),
            data.get('Installs (achieved):', None),
            data.get('Installs (estimated):', None),
            data.get('5 star ratings:', None),
            data.get('4 star ratings:', None),
            data.get('3 star ratings:', None),
            data.get('2 star ratings:', None),
            data.get('1 star ratings:', None),
            data.get('Rank', None),
            data.get('ID', None)
        )
        log_sql_query(sql_query)
        cursor.execute(sql_query, values)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error saving application: {e}")

def save_developer(data):
    try:
        conn = pyodbc.connect(json.load(open('config.json'))['connectionString'])
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Developers WHERE dev_id = ?", data.get('ID', None))
        count = cursor.fetchone()[0]
        if count > 0:
            sql_query = '''
                UPDATE Developers
                SET applications = ?,
                    title = ?,
                    country = ?,
                    address = ?,
                    web = ?,
                    rank = ?,
                    total_rating = ?,
                    average_rating = ?,
                    installs = ?
                WHERE dev_id = ?
            '''
        else:
            sql_query = '''
                INSERT INTO Developers ( applications, title, country, address, web, rank, total_rating, average_rating, installs,dev_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
        values = (
            data.get('Applications', None),
            data.get('Title:', None),
            data.get('Country:', None),
            data.get('Address:', None),
            data.get('Web:', None),
            data.get('Rank', None),
            data.get('Total ratings:', None),
            data.get('Average rating:', None),
            data.get('Installs (achieved):', None),
            data.get('ID', None)
        )
        log_sql_query(sql_query)
        cursor.execute(sql_query, values)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error saving developer: {e}")

def scrape_details(b_url, rank, dev_id, applications):
    b_url = f'https://www.androidrank.org/{b_url}'
    response = requests.get(b_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = {}
    data['Rank'] = int(rank.split(".")[0])
    data['ID'] = dev_id
    data['Applications'] = applications
    try:
        tbody = soup.find_all('tbody')[0:5]
        data['ID'] = dev_id.split("/")[-1]
    except:
        tbody = soup.find_all('tbody')[0:1]
    for table in tbody:
        for tr in table.find_all('tr'):
            th = tr.find('th')
            td = tr.find('td')
            if th and td:
                if th.text.strip() == "Developer:" or th.text.strip() == "Category:":
                    developer_a_tag = td.find('a')
                    if developer_a_tag:
                        developer_href = developer_a_tag.get('href')
                        data[th.text.strip()] = developer_href.split("=")[-1]
                else:
                    data[th.text.strip()] = td.text.strip()

    return data

def OpenLink(page, url, proxies_list):
    proxy = get_working_proxy(proxies_list)
    if proxy is None:
        print("Exiting due to no working proxies.")
        logging.info("Exiting due to no working proxies.")
        return False

    log_http_request("GET", url)
    response = requests.get(url, proxies={"http": proxy, "https": proxy})
    while response.status_code == 429:
        print("Too many requests. Changing proxy and waiting...")
        proxy = get_working_proxy(proxies_list)
        if proxy is None:
            print("No working proxies.")
            logging.info("No working proxies. Waiting...")
            time.sleep(120)
            response = requests.get(url)
        else:    
            time.sleep(5)  
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.find_all('tr')
    next_link = soup.find('a', string='Next >')
    Next = (next_link and next_link.name == 'a')
    i = 1
    for tr in trs:
        cells = tr.find_all('td')
        if len(cells) >= 5:
            rank = cells[0].text.strip()
            link = cells[1].find('a')
            dev_id = link.get('href').split('=')[-1] if link else ''
            applications = cells[4].text
            i += 1
            data = scrape_details(link['href'], rank, dev_id, applications)
            while len(data) < 4:
                print("Too many requests. Changing proxy and waiting...")
                proxy = get_working_proxy(proxies_list)
                if proxy is None:
                    print("Exiting due to no working proxies.")
                    logging.info("No working proxies. Waiting...")
                    time.sleep(120)
                time.sleep(5)  
                data = scrape_details(link['href'], rank, dev_id, applications)
            logging.info(data)
            print(data)
            if "ranking" in url:
                save_developer(data)
            else:
                save_application(data)
    return Next

def Developers():
    page = 1
    Next = True
    while Next:
        url = f'https://www.androidrank.org/developers/ranking?&start={page}'
        Next = OpenLink(page, url, proxies_list)
        page += 20
    print("Exiting Developers")
    logging.info("Exiting Developers")

def Applications():
    developers = All_developers()
    print("Developers :",developers)
    for dev in developers:
        print("Getting for Developer :",dev)
        page = 1
        Next = True
        while Next:
            url = f"https://www.androidrank.org/developer?id={dev}"
            Next = OpenLink(page, url, proxies_list)
            page += 20
    print("Exiting Applications")
    logging.info("Exiting Applications")

def Games():
    all_games = ['GAME_ACTION', 'GAME_ADVENTURE', 'GAME_ARCADE', 'GAME_BOARD', 'GAME_CARD', 'GAME_CASINO',
                 'GAME_CASUAL', 'GAME_EDUCATIONAL', 'GAME_FAMILY', 'GAME_MUSIC', 'GAME_PUZZLE', 'GAME_RACING',
                 'GAME_ROLE_PLAYING', 'GAME_SIMULATION', 'GAME_SPORTS', 'GAME_STRATEGY', 'GAME_TRIVIA', 'GAME_WORD']
    for game in all_games:
        page = 1
        Next = True
        while Next:
            url = f"https://www.androidrank.org/android-most-popular-google-play-apps?start={page}&sort=0&price=all&category={game}"
            Next = OpenLink(page, url, proxies_list)
            page += 20
    print("Exiting Games")
    logging.info("Exiting Games")

log_event("Starting spidering...")
Developers()
Applications()
Games()
log_event("Stopping spidering...")
