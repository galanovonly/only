import csv
import time
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_url_for_partial_class_with_selenium(url, class_substring="social-activities"):
    options = Options()
    options.headless = True
    service = Service(executable_path=r"C:\Users\User\PycharmProjects\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)  # Adjust time as needed to ensure the page is fully loaded

    try:
        # Use CSS selector to find elements that have a class containing the specified substring
        elements = driver.find_elements(By.CSS_SELECTOR, f"[class*='{class_substring}']")
        if elements:
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    return False


def read_urls_from_csv(file_path):
    urls = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                urls.append(row[0].strip())  # Ensuring we strip whitespace here too
    return urls


def main(csv_file_path):
    urls = read_urls_from_csv(csv_file_path)
    urls_with_class = []

    for url in urls:
        url = url.strip('\ufeff').strip()
        print(f"Checking URL: {url}")
        if check_url_for_partial_class_with_selenium(url):
            print(f"The page {url} contains the class 'social-activities'.")
            urls_with_class.append(url)
        else:
            continue
            #print(f"The page {url} does not contain the class 'accent-section__bg'.")
        time.sleep(2)

    print("\nURLs with 'button false fill-alt' class:")
    for url in urls_with_class:
        print(url)


if __name__ == "__main__":
    csv_file_path = r"C:\Users\yourfile.csv"
    main(csv_file_path)
