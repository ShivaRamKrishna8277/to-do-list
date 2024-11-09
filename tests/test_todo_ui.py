from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Path to your chromedriver.exe
DRIVER_PATH = "E:\\to-do-list\\chromedriver.exe"

# Set up Chrome with the driver path using Service
service = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Open the application
driver.get("http://127.0.0.1:8000/static/index.html")  # Pointing to your HTML file served
time.sleep(2)  # Wait for the page to load

# Define functions for adding, editing, and deleting tasks
def add_task(task_name):
    add_task_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "task-input"))
    )
    add_task_input.send_keys(task_name)

    # Click the Add Task button
    add_task_button = driver.find_element(By.ID, "add-task")
    add_task_button.click()

    print(f"Task '{task_name}' added.")

def print_tasks():
    task_elements = driver.find_elements(By.XPATH, "//li")
    for task in task_elements:
        print(task.text)

def edit_task(old_task_name, new_task_name):
    # Wait for the task to appear after adding it
    task_xpath = f"//li[contains(text(), '{old_task_name}')]"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, task_xpath))
    )
    
    task_element = driver.find_element(By.XPATH, task_xpath)
    edit_button = task_element.find_element(By.XPATH, ".//button[contains(text(), 'Edit')]")
    edit_button.click()

    # Wait for the prompt to appear
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    time.sleep(1)  # Optional: Just to ensure the prompt is displayed

    # Send new task name to the prompt
    driver.switch_to.alert.send_keys(new_task_name)
    driver.switch_to.alert.accept()
    
    print(f"Task '{old_task_name}' edited to '{new_task_name}'.")

def delete_task(task_name):
    delete_button = driver.find_element(By.XPATH, f"//li[contains(text(), '{task_name}')]/button[contains(text(), 'Delete')]")
    delete_button.click()
    print(f"Task '{task_name}' deleted.")

# Execute test steps
try:
    add_task("New Task")
    print_tasks()  # Check current tasks after adding
    edit_task("New Task", "Updated Task")
    print_tasks()  # Check current tasks after editing
    delete_task("Updated Task")
    print_tasks()  # Check current tasks after deleting
finally:
    driver.quit()  # Close the browser