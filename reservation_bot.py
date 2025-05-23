# 셀레니움 기본 템블릿
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import time
import random

reservation_complete = False

def check():
    global reservation_complete
    # 크롬 드라이버 생성
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    # 이미지 로딩 비활성화로 속도 향상
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    try:
        day = time.gmtime().tm_mday + 15
        driver = webdriver.Chrome(options=options)

        # url 접속
        driver.get('https://www.zerohongdae.com/reservation/60')
        date = driver.find_element(By.CSS_SELECTOR, f"div[data-date='30'][data-month='4'][data-year='2025']")
        attribute = date.get_attribute("class")

        if "-disabled-" in attribute:
            print(f"{day} : 날짜는 선택불가능")
        else:
            print("이 날짜는 선택가능")
            success = reserve(driver, date)
            if success:
                reservation_complete = True
    except Exception as err:
        print(err)
    finally:
        driver.quit()


def reserve(driver, date):
    print("예약시작")
    date.click()

    wait = WebDriverWait(driver, 5)

    time.sleep(0.015)
    element = wait.until(
        # 테마선택
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#themeChoice > label:nth-child(5)"))
    )
    element.click()

    time.sleep(0.015)

    # 시간선택
    print("시간선택")
    is_enabled_time = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#themeTimeWrap > label:nth-child(7) > input")))
    if is_enabled_time.get_attribute("disabled") is None:
        element2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#themeTimeWrap > label:nth-child(7)")))
        element2.click()
        nextButton = wait.until(EC.element_to_be_clickable((By.ID, "nextBtn")))
        nextButton.click()

        name = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".el-input.bs-bb:nth-child(1)")))
        # name.send_keys("김은지")
        text = "이동호"
        for char in text:
            name.send_keys(char)
            time.sleep(random.uniform(0.025, 0.05))
        # name.send_keys("이동호")
        name.send_keys(Keys.TAB)

        phone = driver.switch_to.active_element
        # phone = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='phone']")))
        # phone.send_keys("01068885740")
        phone_text = "01048196169"
        for char in phone_text:
            phone.send_keys(char)
            time.sleep(random.uniform(0.015, 0.02))

        select_element = wait.until(EC.presence_of_element_located((By.ID, "step2PeopleWrap")))
        select = Select(select_element)
        select.select_by_value("2")

        checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".el-rc.fw7")))
        checkbox.click()

        # submit = wait.until(EC.element_to_be_clickable((By.ID, "reservationBtn")))
        # submit.click()

        print("예약 성공!")
        return True
    else:
        print("해당 시간은 아직 비활성화 상태입니다.")
        return False

def midnight_task():
    global reservation_complete

    for attempt in range(1, 10):
        reservation_complete = False

        try:
            check()
            if reservation_complete:
                break
        except Exception as err:
            print(f"실패: {err}")


if __name__ == "__main__":
    # check()
    schedule.every().day.at("16:55").do(midnight_task)
    # schedule.every(1).seconds.do(check)

    while True:
        schedule.run_pending()
        # time.sleep(1)
