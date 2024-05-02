from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_driver_path = r'C:\Users\User\PycharmProjects\chromedriver.exe'
driver = webdriver.Chrome(service=Service(chrome_driver_path))
driver.get("https://test.test/dashboard/content/pages/test")

# Wait for a fixed time to manually log in
print("Please log in...")
time.sleep(30)  # Adjust this time based on how long it takes to log in

# Find all input fields and textarea elements
input_fields = driver.find_elements(By.XPATH, "//input | //textarea")

# Clear all input fields and textarea elements
for input_field in input_fields:
    try:
        if input_field.is_enabled() and input_field.is_displayed():
            # Scroll the page to bring the input field into view
            actions = ActionChains(driver)
            actions.move_to_element(input_field).perform()
            # Click on the input field using JavaScript
            driver.execute_script("arguments[0].click();", input_field)
            # Move the cursor to the end of the input field's value using JavaScript
            driver.execute_script("arguments[0].selectionStart = arguments[0].selectionEnd = arguments[0].value.length;", input_field)
            # Send a sequence of backspace key presses to clear the input field or textarea
            input_field.send_keys(Keys.BACKSPACE * len(input_field.get_attribute("value")))
            # Introduce a delay after clearing each input field if needed
            # time.sleep(1)
    except Exception as e:
        print(f"An error occurred while clearing input field: {e}")

# Find and click buttons with the word "удалить"
"""
delete_buttons = driver.find_elements(By.XPATH, "//*[contains(text(),'удалить')]")
for delete_button in delete_buttons:
    try:
        delete_button.click()
    except Exception as e:
        print(f"An error occurred while clicking delete button: {e}")
"""

input("Press Enter to quit the script and close the browser...")
driver.quit()
