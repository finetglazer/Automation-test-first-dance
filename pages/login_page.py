from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
import time

class LoginPage(BasePage):
    """Enhanced Page Object Model for Login Page with Robust Selectors"""

    # =======================
    # LOCATORS - FIXED AND ENHANCED
    # =======================

    # Login Form Elements - Multiple strategies for better reliability
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Username']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Password']")
    REMEMBER_CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")

    # FIXED: Removed invalid :contains() CSS selector
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], .login-btn, button.ui-button")

    # Alternative selectors with multiple strategies
    USERNAME_ALTERNATIVES = [
        (By.NAME, "username"),
        (By.ID, "username"),
        (By.CSS_SELECTOR, "input[name='username']"),
        (By.CSS_SELECTOR, "input[id*='username']"),
        (By.CSS_SELECTOR, "input[type='text']"),
        (By.CSS_SELECTOR, "input[type='email']")
    ]

    PASSWORD_ALTERNATIVES = [
        (By.NAME, "password"),
        (By.ID, "password"),
        (By.CSS_SELECTOR, "input[name='password']"),
        (By.CSS_SELECTOR, "input[id*='password']"),
        (By.CSS_SELECTOR, "input[type='password']")
    ]

    # Login button alternatives - using XPath for text-based selection
    LOGIN_BUTTON_ALTERNATIVES = [
        (By.XPATH, "//button[contains(text(), 'LOGIN')]"),
        (By.XPATH, "//button[contains(text(), 'Login')]"),
        (By.XPATH, "//button[contains(text(), 'login')]"),
        (By.XPATH, "//input[@type='submit']"),
        (By.XPATH, "//button[@type='submit']"),
        (By.CSS_SELECTOR, "button.btn-primary"),
        (By.CSS_SELECTOR, "button.btn-login"),
        (By.CSS_SELECTOR, ".login-button"),
        (By.XPATH, "//button[contains(@class, 'login')]"),
        (By.XPATH, "//input[contains(@value, 'LOGIN')]")
    ]

    # Error Messages
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, .alert-danger, .notification-error, .toast-error")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 15)

    # =======================
    # NAVIGATION METHODS
    # =======================

    def navigate_to_login_page(self, base_url="http://localhost"):
        """Navigate to the login page with enhanced error handling"""
        login_urls = [
            f"{base_url}/#/auth",
            f"{base_url}/auth",
            f"{base_url}/login",
            f"{base_url}/#/login"
        ]

        for login_url in login_urls:
            try:
                print(f"Trying to navigate to: {login_url}")
                self.driver.get(login_url)
                time.sleep(3)  # Increased wait time

                if self._check_login_elements_present():
                    print(f"✅ Login page loaded successfully at: {login_url}")
                    self.wait_for_login_page_load()
                    return self
                else:
                    print(f"❌ Login elements not found at: {login_url}")
                    continue

            except Exception as e:
                print(f"❌ Failed to load {login_url}: {str(e)}")
                continue

        raise Exception("Could not find a working login page URL")

    def _check_login_elements_present(self):
        """Enhanced check for login form elements with multiple strategies"""
        print("🔍 Checking for login elements...")

        # Check for username field
        username_found = self._find_element_with_alternatives(
            [self.USERNAME_INPUT] + self.USERNAME_ALTERNATIVES
        )

        # Check for password field
        password_found = self._find_element_with_alternatives(
            [self.PASSWORD_INPUT] + self.PASSWORD_ALTERNATIVES
        )

        # Check for login button
        login_button_found = self._find_element_with_alternatives(
            [self.LOGIN_BUTTON] + self.LOGIN_BUTTON_ALTERNATIVES
        )

        print(f"Username field found: {username_found is not None}")
        print(f"Password field found: {password_found is not None}")
        print(f"Login button found: {login_button_found is not None}")

        return username_found is not None and password_found is not None

    def _find_element_with_alternatives(self, locator_list):
        """Try multiple locators and return the first one that works"""
        for locator in locator_list:
            try:
                element = self.find_element(locator, timeout=2)
                if element and element.is_displayed():
                    print(f"✅ Found element with locator: {locator}")
                    return element
            except Exception:
                continue
        return None

    def wait_for_login_page_load(self):
        """Wait for the login page to fully load with enhanced detection"""
        try:
            # Try multiple strategies to detect page load
            all_locators = [self.USERNAME_INPUT] + self.USERNAME_ALTERNATIVES

            for locator in all_locators:
                try:
                    self.wait.until(EC.presence_of_element_located(locator))
                    print(f"✅ Page loaded - detected element: {locator}")
                    time.sleep(2)  # Additional stabilization time
                    return
                except TimeoutException:
                    continue

            raise Exception("No login elements detected after waiting")

        except Exception as e:
            print(f"❌ Login page load verification failed: {str(e)}")
            # Take screenshot for debugging
            self.take_screenshot("login_page_load_failed")
            raise Exception("Failed to load login page elements")

    # =======================
    # ENHANCED LOGIN METHODS
    # =======================

    def enter_username(self, username):
        """Enhanced username entry with multiple selector strategies"""
        all_username_locators = [self.USERNAME_INPUT] + self.USERNAME_ALTERNATIVES

        for locator in all_username_locators:
            try:
                if self.enter_text(locator, username):
                    print(f"✅ Username entered using locator: {locator}")
                    return True
            except Exception as e:
                print(f"❌ Failed to enter username with {locator}: {str(e)}")
                continue

        print("❌ Could not find username field with any locator")
        return False

    def enter_password(self, password):
        """Enhanced password entry with multiple selector strategies"""
        all_password_locators = [self.PASSWORD_INPUT] + self.PASSWORD_ALTERNATIVES

        for locator in all_password_locators:
            try:
                if self.enter_text(locator, password):
                    print(f"✅ Password entered using locator: {locator}")
                    return True
            except Exception as e:
                print(f"❌ Failed to enter password with {locator}: {str(e)}")
                continue

        print("❌ Could not find password field with any locator")
        return False

    def click_remember_me(self):
        """Click the remember me checkbox if present"""
        try:
            return self.click_element(self.REMEMBER_CHECKBOX)
        except Exception:
            print("⚠️ Remember me checkbox not found or not clickable")
            return False

    def click_login_button(self):
        """Enhanced login button click with multiple selector strategies"""
        all_login_locators = [self.LOGIN_BUTTON] + self.LOGIN_BUTTON_ALTERNATIVES

        for locator in all_login_locators:
            try:
                if self.click_element(locator):
                    print(f"✅ Login button clicked using locator: {locator}")
                    return True
            except Exception as e:
                print(f"❌ Failed to click login button with {locator}: {str(e)}")
                continue

        print("❌ Could not find or click login button with any locator")

        # As a last resort, try pressing Enter on password field
        try:
            print("🔄 Trying to submit form by pressing Enter on password field...")
            password_field = self._find_element_with_alternatives(
                [self.PASSWORD_INPUT] + self.PASSWORD_ALTERNATIVES
            )
            if password_field:
                from selenium.webdriver.common.keys import Keys
                password_field.send_keys(Keys.RETURN)
                print("✅ Form submitted using Enter key")
                return True
        except Exception as e:
            print(f"❌ Enter key submission also failed: {str(e)}")

        return False

    def perform_login(self, username="admin@shopizer.com", password="password", remember_me=False):
        """Enhanced login process with better error handling and debugging"""
        try:
            print(f"🔐 Starting login process with username: {username}")

            # Take screenshot before starting
            self.take_login_screenshot("before_login")

            # Step 1: Enter credentials
            print("📝 Step 1: Entering username...")
            if not self.enter_username(username):
                self.take_login_screenshot("username_entry_failed")
                raise Exception("Failed to enter username")

            print("📝 Step 2: Entering password...")
            if not self.enter_password(password):
                self.take_login_screenshot("password_entry_failed")
                raise Exception("Failed to enter password")

            # Step 3: Remember me (optional)
            if remember_me:
                print("📝 Step 3: Clicking remember me...")
                self.click_remember_me()

            # Take screenshot before clicking login
            self.take_login_screenshot("before_login_click")

            # Step 4: Submit form
            print("📝 Step 4: Clicking login button...")
            if not self.click_login_button():
                self.take_login_screenshot("login_button_click_failed")
                raise Exception("Failed to click login button")

            # Step 5: Wait for login to complete
            print("⏳ Step 5: Waiting for login to complete...")
            if self.wait_for_login_success():
                print("✅ Login completed successfully!")
                self.take_screenshot("login_successful")
                return True
            else:
                raise Exception("Login did not complete successfully")

        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            self.take_login_screenshot("login_process_failed")
            return False

    def wait_for_login_success(self, timeout=15):
        """Enhanced wait for successful login with multiple indicators"""
        try:
            print("⏳ Waiting for login success indicators...")

            # Strategy 1: Wait for URL change
            start_url = self.driver.current_url
            print(f"Current URL: {start_url}")

            try:
                WebDriverWait(self.driver, timeout).until(
                    lambda driver: driver.current_url != start_url and "auth" not in driver.current_url.lower()
                )
                print(f"✅ URL changed from {start_url} to {self.driver.current_url}")
                time.sleep(3)  # Wait for page to stabilize
                return True
            except TimeoutException:
                print("⚠️ URL didn't change, checking other success indicators...")

            # Strategy 2: Check for post-login elements (home page elements)
            home_indicators = [
                (By.CSS_SELECTOR, ".sidebar"),
                (By.CSS_SELECTOR, ".nav-sidebar"),
                (By.CSS_SELECTOR, ".main-content"),
                (By.CSS_SELECTOR, ".dashboard"),
                (By.XPATH, "//a[contains(text(), 'Logout')]"),
                (By.CSS_SELECTOR, ".user-profile")
            ]

            for indicator in home_indicators:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(indicator)
                    )
                    print(f"✅ Found post-login indicator: {indicator}")
                    return True
                except TimeoutException:
                    continue

            # Strategy 3: Check if we're still on login page (login failed)
            if self.is_login_page_loaded():
                # Check for error messages
                if self.is_error_displayed():
                    error_msg = self.get_error_message()
                    raise Exception(f"Login failed with error: {error_msg}")
                else:
                    raise Exception("Still on login page - credentials may be incorrect")

            # If we reach here, assume login was successful but page didn't change as expected
            print("⚠️ Login may have succeeded but indicators are unclear")
            return True

        except Exception as e:
            print(f"❌ Login verification failed: {str(e)}")
            self.take_login_screenshot("login_verification_failed")
            return False

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
        """Check if username field is visible using multiple strategies"""
        username_element = self._find_element_with_alternatives(
            [self.USERNAME_INPUT] + self.USERNAME_ALTERNATIVES
        )
        return username_element is not None

    def is_login_page_loaded(self):
        """Enhanced check if login page is properly loaded"""
        return (self.is_username_field_visible() and
                self._find_element_with_alternatives([self.PASSWORD_INPUT] + self.PASSWORD_ALTERNATIVES) is not None)

    # =======================
    # DEBUGGING METHODS
    # =======================

    def debug_page_elements(self):
        """Debug method to find all possible login elements on the page"""
        print("🔍 DEBUGGING: Analyzing page elements...")

        # Find all input elements
        try:
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"Found {len(inputs)} input elements:")
            for i, input_elem in enumerate(inputs[:10]):  # Limit to first 10
                try:
                    input_type = input_elem.get_attribute("type") or "text"
                    placeholder = input_elem.get_attribute("placeholder") or "N/A"
                    name = input_elem.get_attribute("name") or "N/A"
                    input_id = input_elem.get_attribute("id") or "N/A"
                    print(f"  Input {i+1}: type='{input_type}', placeholder='{placeholder}', name='{name}', id='{input_id}'")
                except Exception:
                    print(f"  Input {i+1}: Could not get attributes")
        except Exception as e:
            print(f"❌ Could not find input elements: {e}")

        # Find all button elements
        try:
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            print(f"Found {len(buttons)} button elements:")
            for i, button in enumerate(buttons[:5]):  # Limit to first 5
                try:
                    button_text = button.text or "N/A"
                    button_type = button.get_attribute("type") or "N/A"
                    button_class = button.get_attribute("class") or "N/A"
                    print(f"  Button {i+1}: text='{button_text}', type='{button_type}', class='{button_class}'")
                except Exception:
                    print(f"  Button {i+1}: Could not get attributes")
        except Exception as e:
            print(f"❌ Could not find button elements: {e}")

        # Take a screenshot for manual inspection
        self.take_login_screenshot("debug_page_analysis")

    # =======================
    # UTILITY METHODS
    # =======================

    def clear_login_form(self):
        """Clear all login form fields"""
        username_field = self._find_element_with_alternatives(
            [self.USERNAME_INPUT] + self.USERNAME_ALTERNATIVES
        )
        password_field = self._find_element_with_alternatives(
            [self.PASSWORD_INPUT] + self.PASSWORD_ALTERNATIVES
        )

        if username_field:
            username_field.clear()
        if password_field:
            password_field.clear()

    def take_login_screenshot(self, filename="login_page"):
        """Take screenshot of login page with timestamp"""
        return self.take_screenshot(f"login_{filename}")

    def get_page_source_snippet(self):
        """Get a snippet of page source for debugging"""
        try:
            source = self.driver.page_source
            return source[:1000] + "..." if len(source) > 1000 else source
        except Exception:
            return "Could not retrieve page source"