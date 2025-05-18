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
    # Логин
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("ivanov")
    driver.find_element(By.NAME, "password").send_keys("1234pass")
    driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()
    time.sleep(2)

    driver.get("http://127.0.0.1:8000/survey/2/")
    time.sleep(1)

    # Отмечаем по одному ответу для каждого вопроса
    radio_buttons = driver.find_elements(By.XPATH, "//input[@type='radio']")
    used_names = set()
    for rb in radio_buttons:
        name = rb.get_attribute("name")
        if name not in used_names:
            rb.click()
            used_names.add(name)
            time.sleep(0.3)

    driver.find_element(By.XPATH, "//button[contains(text(),'Отправить')]").click()
    time.sleep(2)

    # Проверяем, что попали на страницу благодарности
    if "Спасибо за участие" in driver.page_source:
        print("✅ Тест 3: Отзыв отправлен корректно — ПРОЙДЕН")
    else:
        print("❌ Тест 3: Отзыв — НЕ ПРОЙДЕН (не дошёл до страницы благодарности)")

except Exception as e:
    print("❌ Тест 3: УПАЛ С ОШИБКОЙ:", e)

finally:
    driver.quit()
