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
    # Шаг 1 — логин
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("ivanov")
    driver.find_element(By.NAME, "password").send_keys("1234pass")
    driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()
    time.sleep(2)

    # Шаг 2 — переход на несуществующий опрос
    driver.get("http://127.0.0.1:8000/survey/9999/")
    time.sleep(2)

    # Проверка: 404 или сообщение об ошибке
    if "не найден" in driver.page_source or "404" in driver.page_source:
        print("✅ Тест 2.1: Переход на несуществующий опрос — ПРОЙДЕН (ошибка отображается)")
    else:
        print("❌ Тест 2.1: Переход на несуществующий опрос — НЕ ПРОЙДЕН (ошибка не обнаружена)")

except Exception as e:
    print("❌ Тест 2.1: Страница 404 приложения не появилась:", e)

finally:
    driver.quit()

