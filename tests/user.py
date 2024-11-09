import pytest
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

# Test function for login, using pytest parameters
@pytest.mark.parametrize("username, password, expected_result", [
    ("standard_user", "secret_sauce", "success"),  # Valid user
    ("locked_out_user", "secret_sauce", "failure"),  # Locked out user
    ("problem_user", "secret_sauce", "success"),  # Valid user with issues
    ("performance_glitch_user", "secret_sauce", "success"),  # Valid user with glitches
    ("error_user", "secret_sauce", "failure"),  # Invalid user
    ("visual_user", "secret_sauce", "failure")  # Visual issues or special case
])
def test_login(driver, username, password, expected_result):
    """
    Attempts to log in with provided username and password, then checks if the result matches the expected outcome.
    """
    print(f"Attempting login for username: {username}")

    # Open the Sauce Demo website
    driver.get("https://www.saucedemo.com/")

    # Enter username and password, then click login
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # Check for successful login or an error message based on expected result
    try:
        # Look for an element that indicates a successful login
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        # Assert success if expected result is 'success'
        assert expected_result == 'success', f"Expected failure for {username}, but login succeeded unexpectedly."
        print(f"Login successful for user: {username}")
    except Exception:
        # If login fails, check that the expected result is 'failure'
        assert expected_result == 'failure', f"Expected success for {username}, but login failed unexpectedly."
        print(f"Login failed for user: {username}")