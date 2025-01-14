import csv
import time
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class_substrings = [
    "class1",
    "class2",
    "class3",
    "class4",
    "class5"
]


def check_url_for_partial_class_with_selenium(url, class_substrings):
    options = Options()
    options.headless = True
    service = Service(executable_path=r"C:\Users\galan\PycharmProjects\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    #time.sleep(5)  # Adjust time as needed to ensure the page is fully loaded

    found_classes = []
    try:
        for class_substring in class_substrings:
            # Use CSS selector to find elements that have a class containing the specified substring
            elements = driver.find_elements(By.CSS_SELECTOR, f"[class*='{class_substring}']")
            if elements:
                found_classes.append(class_substring)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    return found_classes


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
    urls_with_classes = {class_substring: [] for class_substring in class_substrings}

    for url in urls:
        url = url.strip('\ufeff').strip()
        print(f"Checking URL: {url}")
        found_classes = check_url_for_partial_class_with_selenium(url, class_substrings)
        if found_classes:
            print(f"The page {url} contains the classes: {', '.join(found_classes)}.")
            for found_class in found_classes:
                urls_with_classes[found_class].append(url)
        #time.sleep(2)

    for class_substring, urls in urls_with_classes.items():
        if urls:
            print(f"\nURLs with class substring '{class_substring}':")
            for url in urls:
                print(url)


if __name__ == "__main__":
    csv_file_path = r"C:\Users\user\Desktop\directory\your_file.csv"
    main(csv_file_path)
