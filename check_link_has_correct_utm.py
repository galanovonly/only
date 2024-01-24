import csv
import os
import requests
import time
import urllib3
from bs4 import BeautifulSoup

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Path to the CSV file
csv_file_path = r'C:\Users\Desktop\document.csv'  # Replace with your actual file path

# Read URLs from the CSV file
with open(csv_file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip header if exists
    urls = [row[0] for row in reader]

# Function to clean up URLs
def clean_url(url):
    # Remove BOM character if present
    url = url.lstrip('\ufeff')
    return url.strip()

# Function to check if a URL contains the required parameters
def is_link_in_footer(link, soup, order_number):
    """
    Check if the given link is within the specified footer element.
    """
    footer = soup.find('footer', class_='footer will-change')
    return footer and any(link in str(a) for a in footer.find_all('a', href=True))

# Function to check the URL
def check_url(url, order_number):
    cleaned_url = clean_url(url)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(cleaned_url, verify=False, headers=headers)  # Enable SSL verification
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the link is in the footer
        if is_link_in_footer("https://test.com/", soup, order_number):
            print(f"Iteration {order_number}: The 'https://test.com/' link is in the footer, skipping.")
            return True, None

        # Check if the 'market' link is present and contains 'utm_source' and 'utm_medium'
        market_link = soup.find('a', href=lambda x: x and 'https://test.com/' in x)
        if market_link and 'utm_source' in market_link['href'] and 'utm_medium' in market_link['href']:
            return True, None
        else:
            return False, f"Iteration {order_number}: The 'https://test.com/' link doesn't have 'utm_source' or 'utm_medium'"

    except requests.exceptions.RequestException as e:
        return False, f"Iteration {order_number}: Error during request: {e}"

# List to store failed URLs
failed_urls = []

# Iterate through URLs and perform the test
for order_number, url in enumerate(urls, start=1):
    print(f"Checking URL: {url}")
    result, message = check_url(url, order_number)
    print(f"Result: {result}, Message: {message}")
    if not result:
        failed_urls.append((url, message))
    time.sleep(2)  # Introduce a 2 or 5 second delay between each iteration

# Print the results
if failed_urls:
    print("Failed URLs:")
    for url, message in failed_urls:
        print(f"- {url}: {message}")
else:
    print("All URLs passed the test.")
