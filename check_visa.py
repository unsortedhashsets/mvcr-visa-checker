from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import sys

url_to_check = "https://frs.gov.cz/informace-o-stavu-rizeni/"

load_dotenv()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=2560x2048')
driver = webdriver.Chrome(options=options)

try:
    driver.get(url_to_check)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='12345']")))
    
    visa_string = os.getenv('VISA_STRING')
    if visa_string:
        parts = visa_string.replace('/', '-').split('-')
        parts[1] = parts[1].lstrip('0')
    else:
        sys.exit(3)
    
    input_field_1 = driver.find_element(By.XPATH, "//input[@placeholder='12345']")
    input_field_1.send_keys(parts[1])
    
    input_field_2 = driver.find_element(By.XPATH, "//input[@placeholder='XX']")
    input_field_2.send_keys(parts[2])
    
    dropdowns = driver.find_elements(By.CLASS_NAME, 'react-select__value-container')
    for dropdown, part in zip(dropdowns, parts[3:5]):
        dropdown.click()
        option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{part}']")))
        driver.execute_script("arguments[0].click();", option)
    
    button = driver.find_element(By.CSS_SELECTOR, '.button.button__primary.button--large')
    button.click()
        
    alert_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'alert')))
    classes = alert_element.get_attribute("class").split(' ')
    other_classes = [cls for cls in classes if cls != 'alert']
    
    if 'alert--form-warning' in other_classes:
        print('IN PROGRESS')
    elif 'alert--form-success' in other_classes:
        print('SUCCESS')
    else:
        print('ERROR')
finally:
    driver.quit()