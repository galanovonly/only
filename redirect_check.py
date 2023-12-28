import requests
import urllib3
import time
import csv
import re
from termcolor import colored

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

csv_file_path = r'C:\Users\test.csv'
username = 'username'
password = 'password'

def check_url(url, auth=None):
    try:
        response = requests.get(url, allow_redirects=False, auth=auth, verify=False)
        final_url = response.url
        status_code = response.status_code
        return final_url, status_code
    except Exception as e:
        print(f"Error checking URL {url}: {e}")
        return None, None

def process_url(url):
    #print(f"Processing URL: {url}")

    # Introduce a delay of 1 second between requests
    time.sleep(1)

    # Original URL
    original_url, original_status_code = check_url(url, auth=(username, password))
    print(f"{original_url}, {original_status_code}")
    if not original_url or original_status_code != 200:
        print(colored("Fail", "red"))
    else:
        # Add "index.html" at the end
        index_html_url, index_html_status_code = check_url(url + 'index.html', auth=(username, password))
        print(f"Index.html URL: {index_html_url}, {index_html_status_code}")
        if not index_html_url or index_html_status_code == 200:
            print(colored("Fail", "red"))
        else:
            # Add "index.php" at the end
            index_php_url, index_php_status_code = check_url(url + 'index.php', auth=(username, password))
            print(f"Index.php URL: {index_php_url}, {index_php_status_code}")
            if not index_php_url or index_php_status_code == 200:
                print(colored("Fail", "red"))
            else:
                # Change "https://" to "http://"
                http_url, http_status_code = check_url(re.sub(r'^https://', 'http://', url), auth=(username, password))
                print(f"HTTP URL: {http_url}, {http_status_code}")
                if not http_url or http_status_code == 200:
                    print(colored("Fail", "red"))
                else:
                    # Remove slash "/" at the end
                    no_slash_url, no_slash_status_code = check_url(url.rstrip('/'), auth=(username, password))
                    print(f"No Slash URL: {no_slash_url}, {no_slash_status_code}")
                    if not no_slash_url or no_slash_status_code == 200:
                        print(colored("Fail", "red"))
                    else:
                        # Change "https://" to "https://www."
                        www_url, www_status_code = check_url(re.sub(r'^https://', 'https://www.', url), auth=(username, password))
                        print(f"WWW URL: {www_url}, {www_status_code}")
                        if not www_url or www_status_code == 200:
                            print(colored("Fail", "red"))
                        else:
                            # All possible combinations
                            combinations = [
                                check_url('http://' + url.lstrip('https://').rstrip('/'), auth=(username, password)),
                                check_url('http://www.' + url.lstrip('https://').rstrip('/'), auth=(username, password)),
                                check_url('https://' + url.lstrip('https://').rstrip('/'), auth=(username, password)),
                                check_url('https://www.' + url.lstrip('https://').rstrip('/'),
                                          auth=(username, password)),
                                check_url('http://' + url.lstrip('https://') + 'index.html', auth=(username, password)),
                                check_url('http://' + url.lstrip('https://') + 'index.php', auth=(username, password)),
                                check_url('http://www.' + url.lstrip('https://') + 'index.html',
                                          auth=(username, password)),
                                check_url('http://www.' + url.lstrip('https://') + 'index.php',
                                          auth=(username, password)),
                                check_url('https://www.' + url.lstrip('https://') + 'index.html',
                                          auth=(username, password)),
                                check_url('https://www.' + url.lstrip('https://') + 'index.php',
                                          auth=(username, password)),
                            ]

                            valid_combinations = [comb for comb in combinations if comb[0] and comb[0] != original_url and comb[1] != 200]

                            if not valid_combinations:
                                print(colored("Fail", "red"))

                            print("Valid URLs after redirects:")
                            for valid_url in valid_combinations:
                                print(valid_url)

    print("\n")

with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    urls = [row[0] for row in reader]

print(f"Number of URLs in the CSV file: {len(urls)}")
print("URLs:")
for url in urls:
    process_url(url)
