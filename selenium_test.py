from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

base_url = "http://localhost:5002"

# Initialize WebDriver
driver = webdriver.Firefox()

try:
    # Wait configuration
    wait = WebDriverWait(driver, 10)

    # Test case 1: Register a new user
    def test_register_user():
        driver.get(f"{base_url}/register")
        assert "Register" in driver.title  # Check page title

        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys("newuser")
        password_field.send_keys("newpassword")
        submit_button.click()

        # Wait for a redirect or success message
        time.sleep(2)
        assert "Login" in driver.page_source  # Adjust based on your app's behavior

    # Test case 2: Login with a registered user
    def test_login():
        driver.get(f"{base_url}/login")
        assert "Login" in driver.title  # Check page title

        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys("newuser")
        password_field.send_keys("newpassword")
        submit_button.click()

        # Wait for a redirect or success message
        time.sleep(2)
        assert "Upload" in driver.page_source  # Adjust based on your app's behavior

    # Test case 3: Upload an image after logging in
    def test_upload_image():
        # Assuming user is already logged in
        driver.get(f"{base_url}/upload")
        assert "Upload" in driver.title  # Check page title

        upload_field = driver.find_element(By.NAME, "file")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        upload_field.send_keys("/mnt/ntfs_partition/New folder11/capstone/dataset/ham10000_images_part_2/ISIC_0031309.jpg")  # Provide the correct path to an image
        submit_button.click()

        # Wait for processing
        time.sleep(5)
        assert "Detected Skin Disease" in driver.page_source  # Adjust based on your app's behavior

    # Test case 4: Logout
    def test_logout():
        driver.get(f"{base_url}/logout")
        time.sleep(2)
        assert "Sign In" in driver.page_source  # Adjust based on your app's behavior

    # Execute the test cases
    print("Running test_register_user...")
    test_register_user()
    print("Test register_user passed!")

    print("Running test_login...")
    test_login()
    print("Test login passed!")

    print("Running test_upload_image...")
    test_upload_image()
    print("Test upload_image passed!")

    print("Running test_logout...")
    test_logout()
    print("Test logout passed!")

finally:
    # Close the browser after tests
    driver.quit()
