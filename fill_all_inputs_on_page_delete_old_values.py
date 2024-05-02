from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_driver_path = r'C:\Users\User\PycharmProjects\chromedriver.exe'
driver = webdriver.Chrome(service=Service(chrome_driver_path))
driver.get("https://test.test/dashboard/content/pages/test")

# Wait for a fixed time to manually log in
print("Please log in...")
time.sleep(30)  # Adjust this time based on how long it takes to log in

# Initialize a dictionary to track label counts
label_counts = {}

# Continue with script to fill inputs
labels = driver.find_elements(By.XPATH, "//label")
for label in labels:
    labelText = label.text
    # Check if label text contains any of the words "иконка", "Иконка", or "ИКОНКА"
    if "иконка" in labelText.lower():
        continue
    # Increment count for the label text or start at 1 if not yet encountered
    label_counts[labelText] = label_counts.get(labelText, 0) + 1
    # Generate the new label text with " ТЕСТ" and the count
    newLabelText = f"{labelText} ТЕСТ {label_counts[labelText]}"

    try:
        # Find the following sibling input of each label
        inputField = label.find_element(By.XPATH, "./following-sibling::input")
        if inputField:
            inputField.clear()  # Clear the input field first
            inputField.send_keys(newLabelText)  # Then fill it with the new label text
    except Exception as e:
        print(f"An error occurred for label '{label.text}': {e}")

input("Press Enter to quit the script and close the browser...")
driver.quit()
