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
    # Шаг 2 — переход к конкретному опросу
    driver.get("http://127.0.0.1:8000/survey/1/")
    time.sleep(1)
    # Шаг 3 — отправка пустой формы
    driver.find_element(By.XPATH, "//button[contains(text(),'Отправить')]").click()
    time.sleep(1)

    # Шаг 4 — проверка появления сообщения об ошибке
    page = driver.page_source
    if "обязательно" in page or "ошибка" in page or "заполните" in page or "ответить на все вопросы" in page:
        print("✅ Тест 2: Пустой опрос — ПРОЙДЕН (валидация сработала)")
    else:
        print("❌ Тест 2: Пустой опрос — НЕ ПРОЙДЕН (ошибка не появилась)")

except Exception as e:
    print("❌ Тест 2: УПАЛ С ОШИБКОЙ:", e)

finally:
    driver.quit()
