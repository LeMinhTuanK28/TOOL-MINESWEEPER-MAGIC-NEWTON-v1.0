from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def get_grid_state(driver):
    """Đọc trạng thái lưới Minesweeper từ DOM."""
    try:
        rows, cols = 30, 20
        grid = [[None for _ in range(cols)] for _ in range(rows)]
        
        # Thử tìm lưới bằng các cách khác nhau
        try:
            # Cách 1: Tìm tất cả các ô có lớp .tile hoặc .cell (dựa trên giao diện)
            cells = driver.find_elements(By.CSS_SELECTOR, ".tile, .cell, td")
            if not cells:
                raise Exception("Không tìm thấy ô")
            
            # Ánh xạ tọa độ dựa trên vị trí trong lưới
            cell_index = 0
            for i in range(rows):
                for j in range(cols):
                    if cell_index < len(cells):
                        cell = cells[cell_index]
                        text = cell.text.strip()
                        classes = cell.get_attribute("class").lower()
                        if text in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                            grid[i][j] = int(text)
                        elif "flag" in classes or "mine" in classes:
                            grid[i][j] = "mine"
                        else:
                            grid[i][j] = None
                        cell_index += 1
        except Exception as e:
            print(f"🚫 Lỗi khi đọc lưới: {e}")
            return None
        
        return grid
    except Exception as e:
        print(f"🚫 Lỗi khi đọc lưới: {e}")
        return None

def interact_with_cell(driver, x, y, action):
    """Tương tác với ô tại (x, y): click trái (open_safe) hoặc click phải (mark_mine)."""
    try:
        # Tìm ô dựa trên vị trí trong lưới 30x20
        cells = driver.find_elements(By.CSS_SELECTOR, ".tile, .cell, td")
        if x * 20 + y >= len(cells):
            raise NoSuchElementException(f"Ô ({x}, {y}) vượt quá kích thước lưới")
        
        cell = cells[x * 20 + y]
        
        actions = ActionChains(driver)
        if action == "open_safe":
            actions.click(cell).perform()
            print(f"🟢 Click trái ô ({x}, {y})")
        elif action == "mark_mine":
            actions.context_click(cell).perform()
            print(f"🚩 Click phải ô ({x}, {y})")
        else:
            raise ValueError(f"Hành động không hợp lệ: {action}")
        
        WebDriverWait(driver, 1).until(
            EC.staleness_of(cell) or EC.presence_of_element_located((By.CSS_SELECTOR, ".tile, .cell, td"))
        )
        
        classes = cell.get_attribute("class").lower()
        if action == "mark_mine" and "flag" not in classes:
            print(f"⚠️ Ô ({x}, {y}) không được đánh dấu cờ")
        if action == "open_safe" and "flag" in classes:
            print(f"⚠️ Ô ({x}, {y}) bị đánh dấu cờ, không mở được")
    except NoSuchElementException:
        print(f"🚫 Không tìm thấy ô tại ({x}, {y})")
    except Exception as e:
        print(f"🚫 Lỗi khi tương tác với ô ({x}, {y}): {e}")

def save_screenshot(driver, filename="screenshot.png"):
    """Chụp và lưu ảnh màn hình lưới."""
    try:
        output_dir = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        driver.save_screenshot(os.path.join(output_dir, filename))
        print(f"📸 Đã lưu ảnh chụp màn hình: {filename}")
    except Exception as e:
        print(f"🚫 Lỗi khi lưu ảnh chụp màn hình: {e}")

def log_game_state(message):
    """Ghi log trạng thái trò chơi vào file log.txt nằm ngoài minesweeper_ai."""
    try:
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_file_path = os.path.join(parent_dir, "log.txt")
        with open(log_file_path, "a", encoding="utf-8") as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"🚫 Lỗi khi ghi log: {e}")