from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 브라우저 드라이버 설정 (Chrome 사용 시)
driver = webdriver.Chrome()
# 웹사이트로 이동
url = "https://www.bobaedream.co.kr/mycar/mycar_list.php?gubun=K"
driver.get(url)

# 대기
wait = WebDriverWait(driver, 10)

# 제조사 목록 클릭
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "area-maker")))
manufacturers = driver.find_elements(By.CSS_SELECTOR, "div.area-maker dl.group-list dd")
for manufacturer in manufacturers:
    manufacturer.click()
    time.sleep(1)  # 클릭 후 로딩 대기

    # 모델 목록 가져오기
    models = driver.find_elements(By.CSS_SELECTOR, "div.area-model dl.group-list dd")
    for model in models:
        model.click()
        time.sleep(3)  # 클릭 후 로딩 대기
        print(model.text);
        # 세부 모델 목록 가져오기
        details = driver.find_elements(By.CSS_SELECTOR, "div.area-detail div.group-list dd")
        for detail in details:
            if detail.value_of_css_property("display") != "none":
                try:
                    detail.click()  # 세부 모델 클릭 추가
                    time.sleep(2)   # 클릭 후 로딩 대기
                    
                    labels = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.optBox label"))
                    )
                    for label in labels:
                        print(f"제조사: {manufacturer.text}, 모델: {model.text}, 세부모델: {label.text}")
                except Exception as e:
                    print(f"Label 로딩 오류: {e}")

# 드라이버 종료
driver.quit()
