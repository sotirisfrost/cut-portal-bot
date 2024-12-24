# Website Monitoring Bot

This bot automates the process of monitoring a specific section of a website, detects changes in the data, and sends an email notification when a change is found. It uses Selenium for web automation.

## Features
- Logs into a website.
- Monitors specific data (e.g., GPA, ECTS, completed courses).
- Detects changes by comparing current data with previously stored values.
- Sends an email notification if a change is detected.
- Automatically logs out and logs back in periodically.

---

## Prerequisites

### 1. Install Python
- Download and install Python 3.x from [python.org](https://www.python.org/downloads/).
- Ensure `pip` is installed.

### 2. Install Required Libraries
Run the following command to install the required Python libraries:
```bash
pip install selenium
```

### 3. Download Chrome and ChromeDriver
#### Check Your Google Chrome Version
1. Open Chrome.
2. Go to **Settings** > **About Chrome** and note the version number (e.g., `116.x.x`).

#### Download ChromeDriver
1. Visit the [ChromeDriver downloads page](https://sites.google.com/chromium.org/driver/).
2. Download the version that matches your Chrome browser.
3. Extract the `chromedriver` executable to a folder (e.g., `C:\chromedriver`).

### 4. Set Up Gmail App Password
If you're using Gmail for email notifications:
1. Enable **2-Step Verification** in your Google Account.
2. Generate an **App Password** under [Google Account Security](https://myaccount.google.com/security).
3. Use the generated password in the bot's email configuration.

---

## Configuration

### 1. Update Configuration in the Code
Open `bot.py` and update the following sections:

#### Website Configuration
```python
LOGIN_URL = "https://sis.cut.ac.cy/irj/portal"
USERNAME = "your_username"
PASSWORD = "your_password"
SIDEBAR_BUTTON_XPATH = '//span[contains(text(), "Ακαδημαϊκό Ιστορικό")]'
DATA_FILE = "data_hash.txt"
CHROMEDRIVER_PATH = "C:\\path\\to\\chromedriver.exe"
```

#### Email Configuration
```python
EMAIL_SENDER = "your_email@example.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "recipient_email@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

---

## Running the Bot

### 1. Run the Script
Navigate to the directory containing the `bot.py` file and run:
```bash
python bot.py
```

### 2. Monitor Output
- The bot will periodically check for changes and log relevant messages to the console.
- If a change is detected, the bot will send an email notification and stop.

---

## How It Works
1. Logs into the website using Selenium.
2. Navigates to the specified section.
3. Extracts data and computes its hash.
4. Compares the hash with the previously saved hash in `data_hash.txt`.
5. If a change is detected:
   - Sends an email notification with the updated data.
   - Updates `data_hash.txt` with the new hash.
6. Logs out and waits for 2 minutes before logging back in (you can adapt how long it waits before it logs back in).

---

## Troubleshooting

### Common Issues
#### ChromeDriver Not Found
Ensure the correct path to `chromedriver.exe` is set in the `CHROMEDRIVER_PATH` variable.

#### Gmail SMTP Issues
- Ensure **2-Step Verification** is enabled for your Google account.
- Use an **App Password**, not your regular password.
- Check that "Allow less secure apps" is enabled (if applicable).

#### Website Structure Changes
- If the website's layout changes, update the XPath selectors in the code.
