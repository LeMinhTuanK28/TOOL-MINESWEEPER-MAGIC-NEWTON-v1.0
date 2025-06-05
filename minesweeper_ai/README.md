# 🧠 MagicNewton Minesweeper AI Automation

A professional automation tool built for enterprise use, allowing automated interaction with the **MAGICSWEEPER** game on [MagicNewton](https://magicnewton.com), including:

- ✅ Auto-login via Chrome profile with MetaMask
- 🎯 Auto-launch MAGICSWEEPER and handle play limits
- 🧠 Smart DOM detection (Play Now / No Play Left)
- 🔍 Select game difficulty automatically

---

## 🚀 Features

| Feature                       | Status |
| ----------------------------- | ------ |
| Auto-detect "Play now"        | ✅     |
| DOM scan (no hardcoded XPath) | ✅     |
| Detect "maximum gameplay"     | ✅     |
| Difficulty selection (Expert) | ✅     |
| MetaMask-ready Chrome profile | ✅     |
| Expandable AI grid solver     | 🔄 WIP |

---

## 🛠️ Setup Instructions

### 1. Environment

- Python 3.9+
- Chrome (same version as ChromeDriver)
- Install dependencies:

  ```bash
  pip install selenium
  ```

### 2. Download ChromeDriver

- From: [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)
- Match it with your local Chrome version

### 3. Configure Chrome Profile

- Open Chrome with this flag:

  ```bash
  chrome.exe --user-data-dir="C:/Selenium/Profile 23"
  ```

- Login to:

  - MetaMask
  - MagicNewton

- Ensure login session is saved and close Chrome

### 4. Setup Files

```
/your-folder
├── minesweeper_ai.py
├── link.txt              # contains: https://magicnewton.com/portal/rewards
```

### 5. Run Script

```bash
python minesweeper_ai.py
```

---

## 🧠 Future Plans

- Auto screenshot grid
- Recognize numbers & bombs using OpenCV
- Solve Minesweeper grid automatically
- MetaMask popup auto-confirm

---

## 📁 Folder Structure

```
minesweeper-ai/
    ├── minesweeper_ai.py
    ├── solver.py
    ├── utils.py
    └── README.md
link.txt
page_debug.html
```

---

## 👥 Authors & Credits

- Project Owner: Tuan, Le Minh ✨
- Developer: Tuan, Le Minh

> "Automation is not just about saving time, it's about scaling intelligence."

---

## 📄 License

This project is proprietary and intended for internal enterprise use only.
Contact the project owner for deployment permissions.
