import os
import time
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
LOGIN_URL = "https://sis.cut.ac.cy/irj/portal"
USERNAME = "your_username"
PASSWORD = "your_password"
SIDEBAR_BUTTON_XPATH = '//span[contains(text(), "Ακαδημαϊκό Ιστορικό")]'
DATA_FILE = "data_hash.txt"
CHROMEDRIVER_PATH = "C:\\path\\to\\chromedriver.exe"

# Email Configuration
EMAIL_SENDER = "your_email@example.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "recipient_email@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(subject, body):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def login(driver):
    driver.get(LOGIN_URL)
    time.sleep(5)  # Wait for the page to load

    # Find the username and password fields
    username_field = driver.find_element(By.ID, "logonuidfield")
    password_field = driver.find_element(By.ID, "logonpassfield")

    # Input credentials
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)

    # Click the Log On button
    logon_button = driver.find_element(By.XPATH, '//*[@id="certLogonForm"]/table/tbody/tr[5]/td[2]/input')
    logon_button.click()
    time.sleep(5)  # Wait for login to complete

def navigate_to_academic_history(driver):
    driver.find_element(By.XPATH, SIDEBAR_BUTTON_XPATH).click()
    time.sleep(5)  # Wait for the section to load

def extract_data(driver):
    try:
        # Wait for the GPA element to appear
        gpa_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//td[contains(text(), "Μέσος Όρος")]/following-sibling::td'))
        )
        ects_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//td[contains(text(), "ECTS")]/following-sibling::td'))
        )
        completed_courses_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//td[contains(text(), "Ολοκληρωμένα Επιτυχώς")]/following-sibling::td'))
        )

        return {
            "GPA": gpa_element.text.strip(),
            "ECTS": ects_element.text.strip(),
            "Completed Courses": completed_courses_element.text.strip()
        }
    except Exception as e:
        print(f"Error extracting data: {e}")
        return {}

def check_for_changes(driver):
    login(driver)
    navigate_to_academic_history(driver)

    data = extract_data(driver)
    data_hash = hashlib.md5(str(data).encode()).hexdigest()

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            saved_hash = file.read().strip()
        if saved_hash == data_hash:
            print("No changes detected.")
        else:
            print("Change detected! Sending email notification...")
            with open(DATA_FILE, "w") as file:
                file.write(data_hash)
            
            # Send email notification
            subject = "Change Detected on the Website"
            body = f"The monitored website has changed. Here is the new data:\n\n{data}"
            send_email(subject, body)
            raise SystemExit("Change detected. Stopping bot.")
    else:
        with open(DATA_FILE, "w") as file:
            file.write(data_hash)

def logout(driver):
    # Click the logout button
    logout_button = driver.find_element(By.XPATH, '//*[@id="buttonlogoff"]/span')
    logout_button.click()
    time.sleep(2)  # Allow time for the confirmation dialog to appear

    try:
        # Wait for the "Ναι" button to appear and be clickable
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="button_button_std_yes"]/tbody/tr/td[2]/div'))
        )
        confirm_button.click()
        time.sleep(3)  # Wait for the logout process to complete
    except Exception as e:
        print(f"Error clicking the 'Ναι' button: {e}")

if __name__ == "__main__":
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)  # Initialize the driver once

    while True:  # Infinite loop to keep checking
        try:
            print("Checking for changes...")
            check_for_changes(driver)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Logging out and waiting before retrying...")
            logout(driver)
            time.sleep(120)  # Adapt login time
