from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
import time

class LoginPage(BasePage):
    """Optimized Page Object Model for Login Page with Faster Performance"""

    # =======================
    # OPTIMIZED LOCATORS - Most reliable first
    # =======================

    # Primary selectors (try these first - fastest)
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Username']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], .login-btn, button.ui-button")
    REMEMBER_CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")

    # Backup selectors (only if primary fails)
    USERNAME_BACKUP = (By.NAME, "username")
    PASSWORD_BACKUP = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON_BACKUP = (By.XPATH, "//button[contains(text(), 'LOGIN')]")

    # Error Messages
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, .alert-danger, .notification-error, .toast-error")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 8)  # Reduced from 15 to 8 seconds

    # =======================
    # OPTIMIZED NAVIGATION METHODS
    # =======================

    def navigate_to_login_page(self, base_url="http://localhost"):
        """Optimized navigation - try most likely URL first"""
        try:
            # Based on your success, try the working URL first
            login_url = f"{base_url}/#/auth"
            print(f"🚀 Navigating directly to: {login_url}")

            self.driver.get(login_url)
            time.sleep(2)  # Reduced wait time

            if self._quick_login_check():
                print(f"✅ Login page loaded successfully")
                return self
            else:
                raise Exception("Login elements not found")

        except Exception as e:
            print(f"❌ Fast navigation failed: {str(e)}")
            return self._fallback_navigation(base_url)

    def _quick_login_check(self):
        """Quick check for login elements - optimized for speed"""
        try:
            # Just check for the primary elements quickly
            username = self.find_element(self.USERNAME_INPUT, timeout=3)
            password = self.find_element(self.PASSWORD_INPUT, timeout=2)
            login_btn = self.find_element(self.LOGIN_BUTTON, timeout=2)

            return username is not None and password is not None and login_btn is not None
        except:
            return False

    def _fallback_navigation(self, base_url):
        """Fallback navigation if fast method fails"""
        login_urls = [
            f"{base_url}/auth",
            f"{base_url}/login",
            f"{base_url}/#/login"
        ]

        for login_url in login_urls:
            try:
                print(f"Trying fallback: {login_url}")
                self.driver.get(login_url)
                time.sleep(2)

                if self._quick_login_check():
                    print(f"✅ Fallback successful: {login_url}")
                    return self
            except:
                continue

        raise Exception("Could not find any working login page URL")

    # =======================
    # OPTIMIZED LOGIN METHODS
    # =======================

    def enter_username(self, username):
        """Optimized username entry - try primary selector first"""
        # Try primary selector first (fastest)
        if self.enter_text(self.USERNAME_INPUT, username):
            return True
        # Only try backup if primary fails
        if self.enter_text(self.USERNAME_BACKUP, username):
            return True
        return False

    def enter_password(self, password):
        """Optimized password entry - try primary selector first"""
        # Try primary selector first (fastest)
        if self.enter_text(self.PASSWORD_INPUT, password):
            return True
        # Only try backup if primary fails
        if self.enter_text(self.PASSWORD_BACKUP, password):
            return True
        return False

    def click_login_button(self):
        """Optimized login button click - try primary selector first"""
        # Try primary selector first (fastest)
        if self.click_element(self.LOGIN_BUTTON):
            return True
        # Only try backup if primary fails
        if self.click_element(self.LOGIN_BUTTON_BACKUP):
            return True

        # Last resort: press Enter on password field
        try:
            password_field = self.find_element(self.PASSWORD_INPUT, timeout=2)
            if password_field:
                from selenium.webdriver.common.keys import Keys
                password_field.send_keys(Keys.RETURN)
                return True
        except:
            pass

        return False

    def perform_login(self, username="admin@shopizer.com", password="password", remember_me=False):
        """Optimized login process - streamlined for speed"""
        try:
            print(f"🔐 Quick login with username: {username}")

            # Streamlined process - no extra screenshots for speed
            if not self.enter_username(username):
                raise Exception("Failed to enter username")

            if not self.enter_password(password):
                raise Exception("Failed to enter password")

            if not self.click_login_button():
                raise Exception("Failed to click login button")

            # Optimized wait for login success
            if self.wait_for_login_success():
                print("✅ Login completed successfully!")
                return True
            else:
                raise Exception("Login did not complete successfully")

        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            # Only take screenshot on failure to save time
            self.take_screenshot("login_failed")
            return False

    def wait_for_login_success(self, timeout=10):  # Reduced from 15 to 10
        """Optimized wait for successful login"""
        try:
            start_url = self.driver.current_url

            # Primary strategy: Wait for URL change (fastest indicator)
            try:
                WebDriverWait(self.driver, timeout).until(
                    lambda driver: driver.current_url != start_url and "auth" not in driver.current_url.lower()
                )
                print(f"✅ URL changed - login successful")
                time.sleep(1)  # Minimal stabilization time
                return True
            except TimeoutException:
                pass

            # Secondary check: Look for post-login elements quickly
            post_login_indicators = [
                (By.CSS_SELECTOR, ".sidebar"),
                (By.CSS_SELECTOR, ".main-content"),
                (By.XPATH, "//a[contains(text(), 'Logout')]")
            ]

            for indicator in post_login_indicators:
                try:
                    WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located(indicator)
                    )
                    print(f"✅ Found post-login element: {indicator}")
                    return True
                except TimeoutException:
                    continue

            # If still on auth page, login likely failed
            if "auth" in self.driver.current_url.lower():
                if self.is_error_displayed():
                    error_msg = self.get_error_message()
                    raise Exception(f"Login failed: {error_msg}")
                else:
                    raise Exception("Still on login page - check credentials")

            # Assume success if we got this far
            return True

        except Exception as e:
            print(f"❌ Login verification failed: {str(e)}")
            return False

    # =======================
    # OPTIMIZED VALIDATION METHODS
    # =======================

    def is_error_displayed(self):
        """Quick error check"""
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=2)

    def get_error_message(self):
        """Get error message"""
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_page_loaded(self):
        """Quick login page verification"""
        return self._quick_login_check()

    # =======================
    # UTILITY METHODS
    # =======================

    def take_login_screenshot(self, filename="login_page"):
        """Take screenshot only when needed"""
        return self.take_screenshot(f"login_{filename}")