import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By  # Thêm import By
from utils import get_grid_state, interact_with_cell, save_screenshot, log_game_state

def get_neighbors(x, y, grid, rows=30, cols=20):
    """Lấy danh sách các ô lân cận (8 ô xung quanh) trong lưới."""
    neighbors = []
    for i in range(max(0, x-1), min(rows, x+2)):
        for j in range(max(0, y-1), min(cols, y+2)):
            if (i, j) != (x, y):
                neighbors.append((i, j))
    return neighbors

def logical_deduction(grid):
    """Áp dụng thuật toán suy luận logic để tìm ô an toàn hoặc ô mìn."""
    actions = []
    rows, cols = len(grid), len(grid[0])
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] in [1, 2, 3, 4, 5, 6, 7, 8]:  # Ô có số
                neighbors = get_neighbors(i, j, grid)
                unopened = [n for n in neighbors if grid[n[0]][n[1]] is None]
                mines = [n for n in neighbors if grid[n[0]][n[1]] == "mine"]
                
                if len(unopened) == grid[i][j] - len(mines):
                    for x, y in unopened:
                        if ("mark_mine", x, y) not in actions:
                            actions.append(("mark_mine", x, y))
                
                if len(mines) == grid[i][j]:
                    for x, y in unopened:
                        if ("open_safe", x, y) not in actions:
                            actions.append(("open_safe", x, y))
    
    return actions

def probabilistic_move(grid, total_mines=99):
    """Chọn ô chưa mở với xác suất mìn thấp nhất."""
    unopened = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] is None]
    if not unopened:
        return None
    
    marked_mines = sum(1 for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == "mine")
    remaining_mines = total_mines - marked_mines
    if remaining_mines <= 0:
        return ("open_safe", unopened[0][0], unopened[0][1])
    
    x, y = random.choice(unopened)
    return ("open_safe", x, y)

def solve_minesweeper(driver, max_iterations=100, max_plays=3):
    """Hàm chính để giải Minesweeper, hỗ trợ chơi lại tối đa 3 lần khi GAME OVER."""
    play_count = 0
    while play_count < max_plays:
        play_count += 1
        log_game_state(f"🔄 Bắt đầu lượt chơi {play_count}/3")
        
        rows, cols = 30, 20
        iteration = 0
        
        # Chờ lưới khởi tạo và mở ô đầu tiên
        time.sleep(1)
        start_x, start_y = random.randint(0, rows-1), random.randint(0, cols-1)
        log_game_state(f"🔄 Mở ô đầu tiên ({start_x}, {start_y})")
        interact_with_cell(driver, start_x, start_y, "open_safe")
        time.sleep(2)  # Chờ lưới cập nhật
        
        while iteration < max_iterations:
            grid = get_grid_state(driver)
            if grid is None:
                log_game_state("❌ Không đọc được lưới trò chơi.")
                break
            
            log_game_state(f"Iteration {iteration + 1}:\n{grid_to_string(grid)}")
            
            actions = logical_deduction(grid)
            if not actions:
                log_game_state("ℹ️ Không tìm thấy hành động logic. Thử xác suất...")
                action = probabilistic_move(grid)
                if not action:
                    log_game_state("⚠️ Không còn ô để mở. Dừng lượt chơi.")
                    break
                actions = [action]
            
            for action, x, y in actions:
                interact_with_cell(driver, x, y, action)
                log_game_state(f"Performed {action} at ({x}, {y})")
                time.sleep(0.5)
            
            try:
                page_text = driver.page_source.upper()
                if "YOU WIN" in page_text:
                    log_game_state("🎉 Thắng trò chơi!")
                    save_screenshot(driver, f"game_win_{play_count}.png")
                    return True
                elif "GAME OVER" in page_text:
                    log_game_state("💥 Thua trò chơi!")
                    save_screenshot(driver, f"game_over_{play_count}.png")
                    # Tìm và click nút Play Again
                    try:
                        play_again_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'play again')]"))
                        )
                        play_again_button.click()
                        log_game_state("🟢 Đã click nút Play Again, chuẩn bị lượt tiếp theo")
                        time.sleep(2)  # Chờ giao diện load lại
                        break  # Thoát vòng lặp iteration để bắt đầu lượt mới
                    except TimeoutException:
                        log_game_state("⚠️ Không tìm thấy nút Play Again, dừng chương trình")
                        return False
            except Exception as e:
                log_game_state(f"🚫 Lỗi khi kiểm tra trạng thái: {e}")
            
            iteration += 1
        
        if iteration >= max_iterations:
            log_game_state("⚠️ Đạt giới hạn số vòng lặp trong lượt chơi.")
    
    log_game_state("⚠️ Đã hết 3 lượt chơi. Dừng chương trình.")
    return False

def grid_to_string(grid):
    """Chuyển lưới thành chuỗi để ghi log."""
    result = ""
    for row in grid:
        result += " ".join([str(cell) if cell is not None else "." for cell in row]) + "\n"
    return result