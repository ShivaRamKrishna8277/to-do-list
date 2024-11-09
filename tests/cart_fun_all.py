import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.fixture(scope="module")
def driver():
    # Setup: Initialize the Chrome driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    # Teardown: Close the browser
    driver.quit()

@pytest.mark.parametrize("username, password", [
    ("standard_user", "secret_sauce"),
    ("locked_out_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    ("performance_glitch_user", "secret_sauce"), 
    ("error_user", "secret_sauce"),
    ("visual_user", "secret_sauce"),
])
def test_sauce_cart(driver, username, password):
    # Navigate to the Sauce Demo login page
    driver.get("https://www.saucedemo.com/")

    # Log in using the provided credentials
    username_input = driver.find_element(By.ID, "user-name")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys(username)  # Use the parameterized username
    password_input.send_keys(password)    # Use the parameterized password
    login_button.click()    

    # Wait for the page to load
    time.sleep(5)

    # Add all items to the cart
    add_to_cart_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    for button in add_to_cart_buttons:
        button.click()
        time.sleep(1)  # Wait a moment for the action to register

    # Navigate to the cart
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()

    # Wait for the cart page to load
    time.sleep(5)

    # Get the list of items in the cart
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    item_names = [item.find_element(By.CLASS_NAME, "inventory_item_name").text for item in cart_items]

    # Print the item names
    print(f"Items in the cart for user '{username}':")
    for item_name in item_names:
        print(f"- {item_name}")

    # Assert that the cart contains all items
    # assert len(cart_items) == len(add_to_cart_buttons)