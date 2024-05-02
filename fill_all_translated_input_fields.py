from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
import time

# Translation dictionary
russian_to_english = {
    'Заголовок': 'Title',
    'Текст': 'Text',
    'Название (для метрики)': 'Name (for metric)',
    'Ссылка': 'Link',
    'Alt': 'Alt',
    'Иконка (список кодов)': 'Icon (list of codes)',
    'Подзаголовок': 'Subtitle',
    'Текст ссылки': 'Link text',
    'Адрес ссылки': 'Link address',
    'Текст слева': 'Text on the left',
    'Текст справа': 'Text on the right',
    'Описание': 'Description'
}

chrome_driver_path = r'C:\Users\User\PycharmProjects\chromedriver.exe'
driver = webdriver.Chrome(service=Service(chrome_driver_path))
driver.get("https://test.test/dashboard/content/pages/test")

print("Please log in...")
time.sleep(30)  # Adjust this time based on how long it takes to log in

test_count = 0

# Find all input fields on the page
input_fields = driver.find_elements(By.XPATH, "//input|//textarea")

for field in input_fields:
    # Skip fields based on ID or class
    if "desktopImgcontent-1-content-fields-2-fields-0-3" in field.get_attribute("id") or "input-text-full mt-2" in field.get_attribute("class"):
        continue  # Skip this field

    labelText = ""

    if field.get_attribute("id"):
        label = driver.find_elements(By.XPATH, f"//label[@for='{field.get_attribute('id')}']")
        if label:
            labelText = label[0].text

    if not labelText:
        label = field.find_elements(By.XPATH, ".//ancestor::label")
        if label:
            labelText = label[0].text
        else:
            label = field.find_elements(By.XPATH, "./preceding-sibling::label")
            if label:
                labelText = label[0].text

    # Skip fields with specific label text
    if "иконка" in labelText.lower():
        continue  # Skip this field if label contains "иконка"

    if labelText:
        translated_text = russian_to_english.get(labelText, "TEST")  # Fallback to "TEST" if no translation found
    else:
        translated_text = "TEST"

    try:
        # field.clear()
        test_count += 1
        additional_text = f" TEST {test_count}"
        field.send_keys(translated_text + additional_text)
        time.sleep(1)  # Wait for 1 second after inputting text
    except ElementNotInteractableException as e:
        print(f"Error occurred while filling input field: {e}")
        input("Press Enter to continue...")
        continue  # Move on to the next field
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        break  # Exit the loop on unexpected error

input("Press Enter to quit the script and close the browser...")
driver.quit()
