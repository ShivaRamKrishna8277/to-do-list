import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Fixture to set up and tear down the WebDriver

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_sauce_cart(driver):
    # Navigate to the Sauce Demo login page
    driver.get("https://www.saucedemo.com/")

    # Log in using valid credentials
    username_input = driver.find_element(By.ID, "user-name")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys("standard_user")  # Use valid username
    password_input.send_keys("secret_sauce")  # Use valid password
    login_button.click()

    # Wait for the inventory page to load
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )

    # Add all items to the cart
    add_to_cart_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    for button in add_to_cart_buttons:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(button)).click()
        time.sleep(1)  # Slight delay for each addition to register

    # Navigate to the cart
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()

    # Wait for the cart page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
    )

    # Get the list of items in the cart
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    item_names = [item.find_element(By.CLASS_NAME, "inventory_item_name").text for item in cart_items]

    # Print the item names for verification
    print("Items in the cart:")
    for item_name in item_names:
        print(f"- {item_name}")

    # Assert that the cart contains all items added
    #assert len(cart_items) == len(add_to_cart_buttons), f"Expected {len(add_to_cart_buttons)} items in the cart, but found {len(cart_items)}."
