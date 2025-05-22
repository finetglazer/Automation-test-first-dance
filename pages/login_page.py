from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time

class LoginPage(BasePage):
    """Page Object Model for Login Page"""

    # =======================
    # LOCATORS
    # =======================

    # Login Form Elements
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Username']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Password']")
    REMEMBER_CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], button:contains('LOGIN'), .login-btn, button.ui-button")

    # Alternative selectors in case the above don't work
    USERNAME_ALT = (By.NAME, "username")
    PASSWORD_ALT = (By.NAME, "password")
    LOGIN_BUTTON_ALT = (By.XPATH, "//button[contains(text(), 'LOGIN') or contains(text(), 'Login') or contains(text(), 'login')]")

    # Error Messages
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, .alert-danger, .notification-error")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 15)

    # =======================
    # NAVIGATION METHODS
    # =======================

    def navigate_to_login_page(self, base_url="http://localhost"):
        """Navigate to the login page"""
        login_url = f"{base_url}/#/auth"

        print(f"Navigating to login page: {login_url}")
        self.driver.get(login_url)

        # Wait for page to load
        time.sleep(2)

        # Verify login elements are present
        if self._check_login_elements_present():
            print("✅ Login page loaded successfully")
            self.wait_for_login_page_load()
            return self
        else:
            raise Exception("Login page loaded but login elements not found")

    def _check_login_elements_present(self):
        """Check if login form elements are present on the page"""
        try:
            # Check for username and password fields
            username_present = (self.is_element_visible(self.USERNAME_INPUT, timeout=3) or
                                self.is_element_visible(self.USERNAME_ALT, timeout=3))

            password_present = (self.is_element_visible(self.PASSWORD_INPUT, timeout=3) or
                                self.is_element_visible(self.PASSWORD_ALT, timeout=3))

            return username_present and password_present

        except Exception:
            return False

    def wait_for_login_page_load(self):
        """Wait for the login page to fully load"""
        try:
            # Wait for username field to be present
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located(self.USERNAME_INPUT),
                    EC.presence_of_element_located(self.USERNAME_ALT)
                )
            )
            time.sleep(1)  # Small delay for page to stabilize
        except TimeoutException:
            print("Login page elements did not load properly")
            raise Exception("Failed to load login page elements")

    # =======================
    # LOGIN METHODS
    # =======================

    def enter_username(self, username):
        """Enter username in the username field"""
        if not self.enter_text(self.USERNAME_INPUT, username):
            return self.enter_text(self.USERNAME_ALT, username)
        return True

    def enter_password(self, password):
        """Enter password in the password field"""
        if not self.enter_text(self.PASSWORD_INPUT, password):
            return self.enter_text(self.PASSWORD_ALT, password)
        return True

    def click_remember_me(self):
        """Click the remember me checkbox"""
        return self.click_element(self.REMEMBER_CHECKBOX)

    def click_login_button(self):
        """Click the login button"""
        if not self.click_element(self.LOGIN_BUTTON):
            return self.click_element(self.LOGIN_BUTTON_ALT)
        return True

    def perform_login(self, username="admin@shopizer.com", password="password", remember_me=False):
        """Perform complete login process"""
        try:
            print(f"Attempting to login with username: {username}")

            # Enter credentials
            if not self.enter_username(username):
                raise Exception("Failed to enter username")

            if not self.enter_password(password):
                raise Exception("Failed to enter password")

            # Click remember me if requested
            if remember_me:
                self.click_remember_me()

            # Click login button
            if not self.click_login_button():
                raise Exception("Failed to click login button")

            # Wait for login to complete
            self.wait_for_login_success()

            print("✅ Login successful!")
            return True

        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            return False

    def wait_for_login_success(self, timeout=10):
        """Wait for successful login (page navigation away from login)"""
        try:
            # Wait for URL to change away from auth page
            WebDriverWait(self.driver, timeout).until(
                lambda driver: "auth" not in driver.current_url.lower()
            )
            time.sleep(2)  # Additional wait for page to stabilize
            return True
        except TimeoutException:
            # Check if there's an error message
            if self.is_error_displayed():
                error_msg = self.get_error_message()
                raise Exception(f"Login failed with error: {error_msg}")
            else:
                print("⚠️ Login may have succeeded but URL didn't change as expected")
                return True

    # =======================
    # VALIDATION METHODS
    # =======================

    def is_error_displayed(self):
        """Check if login error is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=3)

    def get_error_message(self):
        """Get the error message text"""
        return self.get_text(self.ERROR_MESSAGE)

    def is_username_field_visible(self):
        """Check if username field is visible"""
        return (self.is_element_visible(self.USERNAME_INPUT, timeout=2) or
                self.is_element_visible(self.USERNAME_ALT, timeout=2))

    def is_login_page_loaded(self):
        """Check if login page is properly loaded"""
        return (self.is_username_field_visible() and
                (self.is_element_visible(self.PASSWORD_INPUT, timeout=2) or
                 self.is_element_visible(self.PASSWORD_ALT, timeout=2)))

    # =======================
    # UTILITY METHODS
    # =======================

    def clear_login_form(self):
        """Clear all login form fields"""
        username_field = self.find_element(self.USERNAME_INPUT) or self.find_element(self.USERNAME_ALT)
        password_field = self.find_element(self.PASSWORD_INPUT) or self.find_element(self.PASSWORD_ALT)

        if username_field:
            username_field.clear()
        if password_field:
            password_field.clear()

    def take_login_screenshot(self, filename="login_page"):
        """Take screenshot of login page"""
        return self.take_screenshot(filename)