import requests
import time
import csv
import re

# Replace with your actual username and password
username = "username"
password = "password"

# Path to the CSV file
csv_file_path = r'C:\Users\pathfile.csv'  # Replace with your actual file path

# Read URLs from the CSV file
with open(csv_file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip header if exists
    urls = [row[0] for row in reader]

# List to store failed URLs
failed_urls = []

# Iterate through each URL
for url in urls:
    # Make a request with basic authentication
    response = requests.get(url, auth=(username, password))
    responseBody = response.text

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Check if the request was redirected
        if response.history:
            print(f"Request for {url} was redirected, skipping...")
            continue  # Skip this URL and move to the next one

        # print(f"Response for {url} is successful")

        while not ('<title>' in responseBody and 'meta property="og:title"' in responseBody):
            # Make another request to get the updated content
            response = requests.get(url, auth=(username, password))
            responseBody = response.text

            # Wait for a short interval before checking again
            time.sleep(2)  # Adjust the interval as needed (in seconds)

        # Continue with your <title> and <h1> check
        # Regular expression for matching <h1> tag with or without attributes
        h1_match = re.search(r'<h1([\s\S]*?)>([\s\S]*?)<\/h1>', responseBody) or re.search(r'<h1>([\s\S]*?)<\/h1>', responseBody)

        # Regular expression for matching <title> tag with specific content
        title_match = re.search(r'<title>([\s\S]*?) text text text <\/title>', responseBody)

        # Regular expression for matching meta property='og:title' tag with specific content
        title_og_match = re.search(r'meta property="og:title" content="([\s\S]*?) text text text',
                                   responseBody)

        if h1_match and title_match:
            print(f"Positive: Both h1_match and title_match are true for {url}")
        elif title_match and title_og_match:
            print(f"Positive: title_match and title_og_match are true, but h1_match is not true for {url}")
        elif title_match:
            print(f"Positive: only title_match is true for {url}")
        else:
            print(f"Negative: Neither Condition 1 nor Condition 2 is true for {url}")
            failed_urls.append(url)
            #+print(responseBody)

    else:
        print(f"Response for {url} is not successful. Status code:", response.status_code)
        failed_urls.append(url)

# Print summary of failed URLs
print("\nSummary of failed URLs:")
for failed_url in failed_urls:
    print(failed_url)
