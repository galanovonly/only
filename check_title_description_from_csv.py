import csv
import requests
import time
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to normalize text (remove extra spaces and convert to lowercase)
def normalize_text(text):
    return ' '.join(text.strip().lower().split())

# Function to compare title or description from CSV with the corresponding tag on the webpage
def compare_tags(tag_from_csv, tag_from_webpage):
    return normalize_text(tag_from_csv) == normalize_text(tag_from_webpage)

# Assuming the CSV structure is: URL in the first column, Title in the second column, Description in the third column
csv_file_path = r'C:\Users\User\Downloads\test.csv'

# Use session for connection pooling and efficiency in requests
session = requests.Session()
# If authentication is needed, uncomment and set it up in the session
# session.auth = ('your_username', 'your_password')

# Read URLs from the CSV file along with corresponding titles and descriptions
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip header if exists
    urls_with_tags = [(row[0], row[1], row[2]) for row in reader]

failed_urls = []

for url, title_tag, description_tag in urls_with_tags:
    # Check if both title and description tags are empty
    if not title_tag and not description_tag:
        print(f"Skipping {url} as both title and description tags are missing.")
        continue

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = session.get(url, headers=headers, timeout=10, verify=False)  # Added timeout for safety
        if response.status_code == 200:
            if response.history:
                print(f"Request for {url} was redirected, skipping...")
                continue

            responseBody = response.text

            # Extract title and description from the HTML response
            title_match = re.search(r'<title>(.*?)<\/title>', responseBody, re.IGNORECASE | re.DOTALL)
            description_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', responseBody, re.IGNORECASE | re.DOTALL)

            # Check if the tags match
            title_match_text = title_match.group(1).strip() if title_match else None
            description_match_text = description_match.group(1).strip() if description_match else None

            if (title_tag and not compare_tags(title_tag, title_match_text)) or \
                    (description_tag and not compare_tags(description_tag, description_match_text)):
                print(f"FAIL: Title or description tag mismatch for {url}")
                if title_tag and not compare_tags(title_tag, title_match_text):
                    print(f"Title from CSV: '{title_tag}', Title from webpage: '{title_match_text}'")
                if description_tag and not compare_tags(description_tag, description_match_text):
                    print(f"Description from CSV: '{description_tag}', Description from webpage: '{description_match_text}'")
                failed_urls.append(url)
            else:
                print(f"{url} OK")
        else:
            print(f"Response for {url} is not successful. Status code: {response.status_code}")
            failed_urls.append(url)
        time.sleep(2)  # Polite delay between requests
    except Exception as e:
        print(f"Error requesting {url}: {e}")
        failed_urls.append(url)

print("\nSummary of failed URLs:")
for failed_url in failed_urls:
    print(failed_url)
