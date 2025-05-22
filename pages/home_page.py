from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time

class HomePage(BasePage):
    """Page Object Model for Home/Dashboard Page"""

    # =======================
    # LOCATORS
    # =======================

    # Language Selector
    LANGUAGE_DROPDOWN = (By.CSS_SELECTOR, "select[name='language'], .language-selector, .lang-selector")
    LANGUAGE_BUTTON = (By.XPATH, "//button[contains(text(), 'Langues') or contains(text(), 'Language')]")
    LANGUAGE_CURRENT = (By.CSS_SELECTOR, ".current-language, .selected-language")

    # Language options
    ENGLISH_OPTION = (By.XPATH, "//option[contains(text(), 'English') or @value='en' or @value='EN']")
    FRENCH_OPTION = (By.XPATH, "//option[contains(text(), 'Français') or contains(text(), 'French') or @value='fr' or @value='FR']")

    # Alternative language selectors (in case it's a different implementation)
    LANGUAGE_LINK_EN = (By.XPATH, "//a[contains(text(), 'English') or contains(text(), 'EN')]")
    LANGUAGE_LINK_FR = (By.XPATH, "//a[contains(text(), 'Français') or contains(text(), 'French') or contains(text(), 'FR')]")

    # Navigation Menu Items
    SIDEBAR_MENU = (By.CSS_SELECTOR, ".sidebar, .nav-sidebar, .main-nav")
    HOME_LINK = (By.XPATH, "//a[contains(text(), 'Accueil') or contains(text(), 'Home')]")

    # Product Management Navigation
    PRODUCTS_MENU = (By.XPATH, "//a[contains(text(), 'Produits') or contains(text(), 'Products')]")
    PRODUCTS_LIST_LINK = (By.XPATH, "//a[contains(@href, 'products') and contains(@href, 'list')]")
    INVENTORY_MENU = (By.XPATH, "//span[contains(text(), 'Gestion des inventaires') or contains(text(), 'Inventory Management')]")

    # User Profile Area
    USER_PROFILE = (By.CSS_SELECTOR, ".user-profile, .admin-user")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Logout') or contains(text(), 'Déconnexion')]")

    # Page Loading Indicators
    LOADING_SPINNER = (By.CSS_SELECTOR, ".spinner, .loading, .loader")
    PAGE_CONTENT = (By.CSS_SELECTOR, ".main-content, .dashboard, .home-content")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 15)

    # =======================
    # NAVIGATION METHODS
    # =======================

    def wait_for_home_page_load(self):
        """Wait for the home page to fully load"""
        try:
            # Wait for main content or sidebar to be present
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located(self.SIDEBAR_MENU),
                    EC.presence_of_element_located(self.PAGE_CONTENT),
                    EC.presence_of_element_located(self.HOME_LINK)
                )
            )
            time.sleep(2)  # Additional wait for page to stabilize
        except TimeoutException:
            print("Home page did not load properly")

    # =======================
    # LANGUAGE METHODS
    # =======================

    def get_current_language(self):
        """Get the currently selected language"""
        try:
            # Check if there's a language dropdown
            dropdown = self.find_element(self.LANGUAGE_DROPDOWN)
            if dropdown:
                selected_option = dropdown.find_element(By.CSS_SELECTOR, "option[selected]")
                return selected_option.text if selected_option else None

            # Check for language button or current language display
            lang_current = self.find_element(self.LANGUAGE_CURRENT)
            if lang_current:
                return lang_current.text

            # Check page content language by looking for French text
            if self.find_element((By.XPATH, "//*[contains(text(), 'Français') or contains(text(), 'Accueil')]")):
                return "French"
            elif self.find_element((By.XPATH, "//*[contains(text(), 'English') or contains(text(), 'Home')]")):
                return "English"

        except Exception as e:
            print(f"Could not determine current language: {e}")

        return "Unknown"

    def is_french_language(self):
        """Check if current language is French"""
        current_lang = self.get_current_language()
        return "french" in current_lang.lower() or "français" in current_lang.lower()

    def is_english_language(self):
        """Check if current language is English"""
        current_lang = self.get_current_language()
        return "english" in current_lang.lower()

    def change_language_to_english(self):
        """Change the language to English"""
        try:
            print("Attempting to change language to English...")

            # Method 1: Try dropdown selection
            if self._try_dropdown_language_change():
                return True

            # Method 2: Try link-based language change
            if self._try_link_language_change():
                return True

            # Method 3: Try button-based language change
            if self._try_button_language_change():
                return True

            print("Could not find language selector")
            return False

        except Exception as e:
            print(f"Failed to change language: {e}")
            return False

    def _try_dropdown_language_change(self):
        """Try to change language using dropdown"""
        try:
            dropdown = self.find_element(self.LANGUAGE_DROPDOWN, timeout=3)
            if dropdown:
                print("Found language dropdown")

                # Click dropdown to open it
                dropdown.click()
                time.sleep(1)

                # Select English option
                english_option = self.find_element(self.ENGLISH_OPTION, timeout=3)
                if english_option:
                    english_option.click()
                    time.sleep(2)
                    print("Selected English from dropdown")
                    return True

        except Exception as e:
            print(f"Dropdown method failed: {e}")
        return False

    def _try_link_language_change(self):
        """Try to change language using link"""
        try:
            english_link = self.find_element(self.LANGUAGE_LINK_EN, timeout=3)
            if english_link:
                print("Found English language link")
                english_link.click()
                time.sleep(2)
                print("Clicked English language link")
                return True

        except Exception as e:
            print(f"Link method failed: {e}")
        return False

    def _try_button_language_change(self):
        """Try to change language using button"""
        try:
            lang_button = self.find_element(self.LANGUAGE_BUTTON, timeout=3)
            if lang_button:
                print("Found language button")
                lang_button.click()
                time.sleep(1)

                # Look for English option in dropdown/menu
                english_option = self.find_element(self.ENGLISH_OPTION, timeout=3)
                if english_option:
                    english_option.click()
                    time.sleep(2)
                    print("Selected English from language menu")
                    return True

        except Exception as e:
            print(f"Button method failed: {e}")
        return False

    def wait_for_language_change(self, timeout=10):
        """Wait for language change to take effect"""
        try:
            # Wait for page to reload or content to change
            WebDriverWait(self.driver, timeout).until(
                lambda driver: not self.is_french_language()
            )
            time.sleep(2)
            return True
        except TimeoutException:
            print("Language change may not have taken effect")
            return False

    # =======================
    # NAVIGATION TO PRODUCTS
    # =======================

    def navigate_to_products_page(self):
        """Navigate to the products list page"""
        try:
            print("Navigating to products page...")

            # Method 1: Try direct URL navigation
            if self._try_direct_products_navigation():
                return True

            # Method 2: Try menu navigation
            if self._try_menu_products_navigation():
                return True

            print("Could not navigate to products page")
            return False

        except Exception as e:
            print(f"Failed to navigate to products: {e}")
            return False

    def _try_direct_products_navigation(self):
        """Try direct URL navigation to products page"""
        try:
            self.driver.get("http://localhost/#/pages/catalogue/products/products-list")
            time.sleep(3)

            # Check if we're on the products page
            if "products" in self.driver.current_url.lower():
                print("Successfully navigated to products page via direct URL")
                return True

        except Exception as e:
            print(f"Direct navigation failed: {e}")
        return False

    def _try_menu_products_navigation(self):
        """Try menu-based navigation to products page"""
        try:
            # Look for products menu
            products_menu = self.find_element(self.PRODUCTS_MENU, timeout=5)
            if products_menu:
                print("Found products menu")
                products_menu.click()
                time.sleep(1)

                # Look for products list link
                products_list = self.find_element(self.PRODUCTS_LIST_LINK, timeout=5)
                if products_list:
                    products_list.click()
                    time.sleep(3)
                    print("Clicked products list link")
                    return True

        except Exception as e:
            print(f"Menu navigation failed: {e}")
        return False

    # =======================
    # UTILITY METHODS
    # =======================

    def is_home_page_loaded(self):
        """Check if home page is properly loaded"""
        return (self.is_element_visible(self.SIDEBAR_MENU, timeout=3) or
                self.is_element_visible(self.HOME_LINK, timeout=3))

    def logout(self):
        """Logout from the application"""
        try:
            logout_btn = self.find_element(self.LOGOUT_BUTTON)
            if logout_btn:
                logout_btn.click()
                time.sleep(2)
                return True
        except Exception as e:
            print(f"Logout failed: {e}")
        return False

    def take_home_screenshot(self, filename="home_page"):
        """Take screenshot of home page"""
        return self.take_screenshot(filename)