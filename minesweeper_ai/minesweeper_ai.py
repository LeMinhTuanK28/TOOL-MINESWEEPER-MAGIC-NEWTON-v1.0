# KHỞI TẠO LỆNH ĐIỀU KHIỂN SELENIUM;
# Có thể tải ChromeDriver tại: https://googlechromelabs.github.io/chrome-for-testing/#stable;
# Đảm bảo rằng đã cài đặt Selenium bằng lệnh: pip install selenium;

# Import các thư viện cần thiết;
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os

# CẤU HÌNH CHROME VỚI PROFILE "JOB SOCCER 2" hoặc "YOUR_PROFILE_NAME";
# Kiểm tra xem đường dẫn profile, version Chrome và ChromeDriver, ... tại đây: Mở chở Chrome bạn muốn kiểm tra -> dán vào tìm kiếm: chrome://version/;
# Lưu ý: Đảm bảo rằng đã cài đặt ChromeDriver tương ứng với phiên bản Chrome của.
chrome_options = Options()
# chrome_options.add_argument("user-data-dir=C:/Users/Admin/AppData/Local/Google/Chrome/User Data")
# chrome_options.add_argument("profile-directory=Profile 23")  # Đổi nếu muốn dùng profile khác;

# Thêm các tùy chọn tránh lỗi crash
profile_path = "C:/Selenium/Profile 23"
if not os.path.exists(profile_path):
    os.makedirs(profile_path)

chrome_options.add_argument(f"user-data-dir={profile_path}")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument("--disable-sync")
chrome_options.add_argument("--disable-translate")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument("--disable-sync")
chrome_options.add_argument("--disable-translate")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")

# Đường dẫn tới ChromeDriver phù hợp với Chrome 137;
CHROMEDRIVER_PATH = "D:\\ChromeDriver\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # sửa đúng đường dẫn nếu cần;

try:
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print("🚫 Không khởi tạo được ChromeDriver:", e)
    sys.exit()

# B1: MỞ TRANG MAGIC NEWTON VỚI ĐƯỜNG DẪN TRONG FILE link.txt;
try:
    with open("link.txt", "r", encoding="utf-8") as f:
        url = f.read().strip()
except Exception as e:
    print("❌ Không đọc được file link.txt:", e)
    driver.quit()
    sys.exit()

# MỞ WEBSITE MAGIC NEWTON;
try:
    driver.get(url)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("🟢 Trang đã load xong")
except Exception as e:
    print("🚫 Không mở được trang:", e)
    driver.quit()
    sys.exit()

# B2: TÌM GAME MAGICSWEEPER VÀ NHẤN "Play now";
try:
    # Chờ khối có chữ MAGICSWEEPER xuất hiện (toàn bộ nội dung)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'MAGICSWEEPER')]"))
    )

    # Sau đó quét toàn bộ DOM để tìm đúng khối có nút Play now
    divs = driver.find_elements(By.CSS_SELECTOR, "div")
    found = False

    for div in divs:
        try:
            text = div.text.upper()
            if "MAGICSWEEPER" in text:
                buttons = div.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    if "PLAY NOW" in btn.text.upper():
                        btn.click()
                        print("🟢 Đã vào trò MAGICSWEEPER (quét DOM sau khi trang load)")
                        found = True
                        break
        except Exception:
            continue

        if found:
            break

    if not found:
        raise Exception("Không tìm thấy nút Play now cho MAGICSWEEPER")

except TimeoutException:
    print("🔴 Trang không load phần MAGICSWEEPER trong thời gian giới hạn.")
    driver.quit()
    sys.exit()
except Exception as e:
    print("🔴 Không tìm thấy nút Play now (tự động):", e)
    with open("page_debug.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    driver.quit()
    sys.exit()

# CHỜ TRÒ CHƠI LOAD XONG TRONG 5 GIÂY;
time.sleep(5)

# B3: KIỂM TRA TRẠNG THÁI LƯỢT CHƠI;
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    page_text = driver.page_source.upper()
    if "MAXIMUM GAMEPLAY REACHED" in page_text or "PLAY AGAIN TOMORROW" in page_text:
        print("⚠️  Đã chơi hết lượt hôm nay. Thoát chương trình.")
        driver.quit()
        sys.exit()
except Exception as e:
    print("⚠️  Không kiểm tra được trạng thái lượt chơi:", e)

# B4: NẾU CÓ NÚT CONTINUE THÌ CLICK;
try:
    continue_button_xpath = "//button[contains(translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONTINUE')]"
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, continue_button_xpath)))
    driver.find_element(By.XPATH, continue_button_xpath).click()
    print("🟢 Đã click nút Continue")
    time.sleep(2)  # chờ giao diện load sau khi bấm
except TimeoutException:
    print("ℹ️ Không có nút Continue – tiếp tục bình thường.")
except Exception as e:
    print("⚠️ Lỗi khi cố click Continue:", e)


# B5: MỞ MENU CHỌN ĐỘ KHÓ;
try:
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains

    print("🔄 Đang dùng phím TAB để đến dòng 'Selected Difficulty'...")

    actions = ActionChains(driver)
    max_tab = 20  # tránh vòng lặp vô hạn;
    found_difficulty = False

    for _ in range(max_tab):
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.2)
        # kiểm tra nội dung phần tử đang được focus;
        focused_text = driver.execute_script("return document.activeElement.innerText;")
        if focused_text.strip().upper().startswith("SELECTED DIFFICULTY"):
            print(f"🔹 Đã focus đến: {focused_text}")
            actions.send_keys(Keys.ENTER).perform()
            found_difficulty = True
            break

    if not found_difficulty:
        raise Exception("Không tìm thấy dòng 'Selected Difficulty' bằng TAB")

    time.sleep(1)

    print("🔄 Đang TAB đến Expert (30×20)...")
    found_expert = False

    for _ in range(10):
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.2)
        focused_text = driver.execute_script("return document.activeElement.innerText;")
        if "EXPERT" in focused_text.upper():
            print(f"🔹 Đã focus đến: {focused_text}")
            actions.send_keys(Keys.ENTER).perform()
            found_expert = True
            break

    if not found_expert:
        raise Exception("Không tìm thấy lựa chọn 'Expert' bằng TAB")

    print("✅ Đã chọn độ khó: Expert (bằng phím TAB)")
    time.sleep(2)
except Exception as e:
    print("🚫 Không chọn được độ khó (phím TAB động):", e)

    
# GIỮ TRÌNH DUYỆT MỞ (tuỳ chọn);
try:
    input("🔵 Nhấn ENTER để đóng trình duyệt và kết thúc...")
except KeyboardInterrupt:
    print("⛔ Đã huỷ bằng Ctrl+C")
finally:
    driver.quit()
