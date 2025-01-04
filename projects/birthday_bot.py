import datetime
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wish_birth(name):
    return "Happy Birthday " + name.split(" ")[0] + "!!"

def getJsonData(file, attr_ret, attr1, attr2, attr_val1, attr_val2):
    data = json.load(file)
    retv = []
    for i in data:
        if i[attr1] == attr_val1 and i[attr2] == attr_val2:
            retv.append(i[attr_ret])
    return retv

print("Script Running")

# Optimized loop with timeout
start_time = datetime.datetime.now()
timeout = 300  # 5 minutes

while True:
    try:
        datt = datetime.datetime.now()
        month = str(datt.month).zfill(2)  # Format month as two digits
        day = str(datt.day).zfill(2)      # Format day as two digits
        with open("birthdays.json", "r") as data_file:
            namev = getJsonData(data_file, "name", "birth_month", "birth_date",
                                month, day)
    except json.decoder.JSONDecodeError:
        time.sleep(1)
        continue

    if namev:
        break

    if (datetime.datetime.now() - start_time).seconds > timeout:
        print("Timeout reached. Exiting.")
        break

chropt = webdriver.ChromeOptions()
chropt.add_argument("--user-data-dir=C:\\Users\\shash\\AppData\\Local\\Google\\Chrome\\User Data")
chropt.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # or the path to your chrome.exe

driver = webdriver.Chrome(service=Service("C:\\Users\\shash\\Downloads\\chromedriver-win64\\chromedriver.exe"), options=chropt)

# Dynamic wait for WhatsApp Web to load
driver.get("https://web.whatsapp.com/")
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CLASS_NAME, "_3NWy8"))  # Update the class as necessary
)

print(f"Birthdays today: {namev}")

# Iterate over contacts and send birthday wishes
for inp in namev:
    try:
        eleNM = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{inp}"]'))
        )
        eleNM.click()
        eleTF = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_13mgZ"))
        )
        eleTF.send_keys(wish_birth(inp))
        eleSND = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_3M-N-"))
        )
        eleSND.click()
    except Exception as ex:
        print(f"Error for {inp}: {ex}")
        continue