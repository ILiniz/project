from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

service = Service("C:\\Users\\user\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
options = Options()
options.binary_location = chrome_path
driver = webdriver.Chrome(service=service, options=options)

try:
    # Шаг 1 — логин в admin
    driver.get("http://127.0.0.1:8000/admin/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("superadmin")
    driver.find_element(By.NAME, "password").send_keys("Snowblind296")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(2)

    # Шаг 2 — переход к добавлению Survey
    driver.get("http://127.0.0.1:8000/admin/polls/survey/add/")
    time.sleep(2)

    # Шаг 3 — оставить поле пустым и нажать Save
    driver.find_element(By.NAME, "_save").click()
    time.sleep(1)

    # Шаг 4 — проверка сообщения об ошибке
    page = driver.page_source
    if "This field is required" in page or "Обязательное поле" in page:
        print("✅ Тест 4.1: Пустое название опроса — ПРОЙДЕН (валидация сработала)")
    else:
        print("❌ Тест 4.1: Пустое название опроса — НЕ ПРОЙДЕН (ошибки нет)")

except Exception as e:
    print("❌ Тест 4.1: УПАЛ С ОШИБКОЙ:", e)

finally:
    driver.quit()
