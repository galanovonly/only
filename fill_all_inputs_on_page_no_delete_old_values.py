from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_driver_path = r'C:\Users\User\PycharmProjects\chromedriver.exe'
driver = webdriver.Chrome(service=Service(chrome_driver_path))
driver.get("https://test.test/dashboard/content/pages/test")

print("Please log in...")
time.sleep(30)  # Consider using explicit waits here as well for better reliability

test_count = 0

input_fields = driver.find_elements(By.XPATH, "//input[@type='text']")
for input_field in input_fields:
    try:
        input_id = input_field.get_attribute("id")
        if input_id and "desktopImgcontent" in input_id:
            continue

        # Check for a preceding sibling label safely
        try:
            label = WebDriverWait(input_field, 2).until(EC.presence_of_element_located((By.XPATH, "./preceding-sibling::label")))
            if label.text.lower() == "иконка":
                continue
        except:
            # No preceding label or doesn't meet criteria
            pass

        test_count += 1
        additional_text = f" ТЕСТ {test_count}"
        current_value = input_field.get_attribute("value")
        new_value = current_value + additional_text if current_value else additional_text
        input_field.clear()
        input_field.send_keys(new_value)
        time.sleep(1)  # Consider a more dynamic wait based on page conditions
    except Exception as e:
        print(f"An error occurred: {e}")

input("Press Enter to quit the script and close the browser...")
# Consider handling the browser quit process here to ensure the browser always closes
