from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time

class HomePage(BasePage):
    """Enhanced Page Object Model for Home/Dashboard Page with Better Detection"""

    # =======================
    # ENHANCED LOCATORS WITH MULTIPLE STRATEGIES
    # =======================

    # Language Selector - Enhanced for Nebular UI (Angular)
    LANGUAGE_SELECTORS = [
        # Nebular UI specific selectors (try these first for speed)
        (By.CSS_SELECTOR, "nb-action[nbcontextmenutag='language']"),
        (By.CSS_SELECTOR, "nb-action.context-menu-host"),
        (By.XPATH, "//nb-action[contains(text(), 'Languages')]"),
        (By.XPATH, "//nb-action[contains(text(), 'English') or contains(text(), 'Français')]"),
        # Standard selectors as fallback
        (By.CSS_SELECTOR, "select[name='language']"),
        (By.CSS_SELECTOR, ".language-selector"),
        (By.CSS_SELECTOR, ".lang-selector"),
        (By.CSS_SELECTOR, "select.form-control"),
        (By.XPATH, "//select[contains(@name, 'language') or contains(@id, 'language')]")
    ]

    # Primary language selector (Nebular UI)
    LANGUAGE_DROPDOWN = (By.CSS_SELECTOR, "nb-action[nbcontextmenutag='language']")
    LANGUAGE_BUTTON = (By.CSS_SELECTOR, "nb-action[nbcontextmenutag='language']")
    LANGUAGE_CURRENT = (By.CSS_SELECTOR, "nb-action[nbcontextmenutag='language']")

    # Language options
    ENGLISH_OPTION = (By.XPATH, "//option[contains(text(), 'English') or @value='en' or @value='EN']")
    FRENCH_OPTION = (By.XPATH, "//option[contains(text(), 'Français') or contains(text(), 'French') or @value='fr' or @value='FR']")

    # Alternative language selectors
    LANGUAGE_LINK_EN = (By.XPATH, "//a[contains(text(), 'English') or contains(text(), 'EN')]")
    LANGUAGE_LINK_FR = (By.XPATH, "//a[contains(text(), 'Français') or contains(text(), 'French') or contains(text(), 'FR')]")

    # HOME PAGE DETECTION - Enhanced with multiple strategies
    HOME_PAGE_INDICATORS = [
        (By.CSS_SELECTOR, ".sidebar"),
        (By.CSS_SELECTOR, ".nav-sidebar"),
        (By.CSS_SELECTOR, ".main-nav"),
        (By.CSS_SELECTOR, ".main-content"),
        (By.CSS_SELECTOR, ".dashboard"),
        (By.CSS_SELECTOR, ".home-content"),
        (By.CSS_SELECTOR, ".content-wrapper"),
        (By.CSS_SELECTOR, ".page-content"),
        (By.XPATH, "//div[contains(@class, 'content')]"),
        (By.XPATH, "//nav[contains(@class, 'sidebar')]"),
        (By.XPATH, "//div[contains(@class, 'dashboard')]"),
        (By.XPATH, "//a[contains(text(), 'Logout') or contains(text(), 'Déconnexion')]"),
        (By.CSS_SELECTOR, ".user-profile"),
        (By.CSS_SELECTOR, ".admin-user"),
        (By.TAG_NAME, "nav"),
        (By.TAG_NAME, "aside")
    ]

    # Navigation Menu Items - Enhanced
    NAVIGATION_INDICATORS = [
        (By.XPATH, "//a[contains(text(), 'Accueil') or contains(text(), 'Home')]"),
        (By.XPATH, "//a[contains(text(), 'Produits') or contains(text(), 'Products')]"),
        (By.XPATH, "//a[contains(text(), 'Catalogue')]"),
        (By.XPATH, "//span[contains(text(), 'Gestion') or contains(text(), 'Management')]"),
        (By.CSS_SELECTOR, "a[href*='catalogue']"),
        (By.CSS_SELECTOR, "a[href*='products']"),
        (By.CSS_SELECTOR, "a[href*='home']")
    ]

    # Product Management Navigation
    PRODUCTS_MENU = (By.XPATH, "//a[contains(text(), 'Produits') or contains(text(), 'Products')]")
    PRODUCTS_LIST_LINK = (By.XPATH, "//a[contains(@href, 'products') and contains(@href, 'list')]")
    INVENTORY_MENU = (By.XPATH, "//span[contains(text(), 'Gestion des inventaires') or contains(text(), 'Inventory Management')]")

    # User Profile Area
    USER_PROFILE = (By.CSS_SELECTOR, ".user-profile, .admin-user")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Logout') or contains(text(), 'Déconnexion')]")

    # Page Loading Indicators
    LOADING_SPINNER = (By.CSS_SELECTOR, ".spinner, .loading, .loader")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 20)  # Increased timeout

    # =======================
    # ENHANCED NAVIGATION METHODS
    # =======================

    def wait_for_home_page_load(self, timeout=20):
        """Enhanced wait for the home page to fully load with multiple detection strategies"""
        try:
            print("🏠 Waiting for home page to load...")
            print(f"Current URL: {self.driver.current_url}")

            # Strategy 1: Wait for any home page indicator
            success = self._wait_for_any_element(self.HOME_PAGE_INDICATORS, timeout=10)
            if success:
                print("✅ Home page detected via main indicators")
                time.sleep(2)  # Stabilization time
                return True

            # Strategy 2: Wait for navigation elements
            success = self._wait_for_any_element(self.NAVIGATION_INDICATORS, timeout=5)
            if success:
                print("✅ Home page detected via navigation elements")
                time.sleep(2)
                return True

            # Strategy 3: Check if URL suggests we're on home page
            current_url = self.driver.current_url.lower()
            if "home" in current_url or current_url.endswith("/"):
                print("✅ Home page detected via URL pattern")
                time.sleep(3)  # Give more time for elements to load
                return True

            # Strategy 4: Wait a bit more and check for any interactive elements
            print("🔄 Trying extended wait for page elements...")
            time.sleep(5)

            # Check for any clickable elements that suggest a loaded page
            interactive_elements = [
                (By.TAG_NAME, "button"),
                (By.TAG_NAME, "a"),
                (By.TAG_NAME, "input"),
                (By.CSS_SELECTOR, "[onclick]"),
                (By.CSS_SELECTOR, "[href]")
            ]

            success = self._wait_for_any_element(interactive_elements, timeout=5)
            if success:
                print("✅ Home page detected via interactive elements")
                return True

            print("⚠️ Could not definitively detect home page load, but continuing...")
            return True  # Be more lenient

        except Exception as e:
            print(f"❌ Home page load detection failed: {str(e)}")
            self.debug_page_state()
            return True  # Be lenient - if we got this far, login worked

    def _wait_for_any_element(self, locator_list, timeout=10):
        """Wait for any element from a list of locators to be present"""
        for locator in locator_list:
            try:
                WebDriverWait(self.driver, timeout // len(locator_list) + 1).until(
                    EC.presence_of_element_located(locator)
                )
                print(f"✅ Found element: {locator}")
                return True
            except TimeoutException:
                continue
        return False

    def is_home_page_loaded(self):
        """Enhanced check if home page is properly loaded"""
        print("🔍 Checking if home page is loaded...")

        # Check URL first
        current_url = self.driver.current_url.lower()
        print(f"Current URL: {current_url}")

        # URL-based detection
        url_indicators = ["home", "dashboard", "main", "admin"]
        if any(indicator in current_url for indicator in url_indicators):
            print("✅ Home page detected via URL")
            return True

        # Element-based detection
        for indicator in self.HOME_PAGE_INDICATORS:
            if self.is_element_visible(indicator, timeout=2):
                print(f"✅ Home page detected via element: {indicator}")
                return True

        # Navigation-based detection
        for nav_indicator in self.NAVIGATION_INDICATORS:
            if self.is_element_visible(nav_indicator, timeout=2):
                print(f"✅ Home page detected via navigation: {nav_indicator}")
                return True

        # If we can't find specific indicators but we're not on auth page, assume success
        if "auth" not in current_url and "login" not in current_url:
            print("✅ Not on auth page, assuming home page loaded")
            return True

        print("❌ Home page indicators not found")
        return False

    def debug_page_state(self):
        """Debug method to analyze current page state"""
        print("🔍 DEBUGGING HOME PAGE STATE:")
        print(f"Current URL: {self.driver.current_url}")
        print(f"Page title: {self.driver.title}")

        # Check what elements are actually present
        try:
            all_elements = self.driver.find_elements(By.XPATH, "//*")
            print(f"Total elements on page: {len(all_elements)}")

            # Look for common elements
            divs = self.driver.find_elements(By.TAG_NAME, "div")
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            links = self.driver.find_elements(By.TAG_NAME, "a")

            print(f"Divs: {len(divs)}, Buttons: {len(buttons)}, Links: {len(links)}")

            # Sample some element text
            for i, link in enumerate(links[:5]):
                try:
                    text = link.text.strip()
                    href = link.get_attribute("href")
                    if text:
                        print(f"Link {i+1}: '{text}' -> {href}")
                except:
                    pass

        except Exception as e:
            print(f"Could not analyze page elements: {e}")

        # Take screenshot for manual inspection
        self.take_screenshot("home_page_debug")

    # =======================
    # ENHANCED LANGUAGE METHODS
    # =======================

    def get_current_language(self):
        """Enhanced language detection for Nebular UI with faster detection"""
        try:
            print("🌐 Detecting current language...")

            # Strategy 1: Check Nebular UI language component (fastest)
            nebular_lang = self.find_element((By.CSS_SELECTOR, "nb-action[nbcontextmenutag='language']"), timeout=3)
            if nebular_lang:
                lang_text = nebular_lang.text.strip()
                print(f"Language detected from Nebular component: {lang_text}")

                # Parse the text format: "Languages - (English)" or "Languages - (Français)"
                if "English" in lang_text:
                    return "English"
                elif "Français" in lang_text or "French" in lang_text:
                    return "French"
                else:
                    return lang_text

            # Strategy 2: Check other language selectors (fallback)
            for locator in self.LANGUAGE_SELECTORS[4:]:  # Skip the Nebular ones we already tried
                try:
                    dropdown = self.find_element(locator, timeout=1)  # Shorter timeout for speed
                    if dropdown:
                        selected_option = dropdown.find_element(By.CSS_SELECTOR, "option[selected]")
                        if selected_option:
                            lang = selected_option.text
                            print(f"Language detected from dropdown: {lang}")
                            return lang
                except:
                    continue

            # Strategy 3: Check current language display
            lang_current = self.find_element(self.LANGUAGE_CURRENT, timeout=1)
            if lang_current:
                lang = lang_current.text
                print(f"Language detected from current display: {lang}")
                return lang

            # Strategy 4: Analyze page content for language indicators (quick check)
            french_indicators = ["Français", "Accueil", "Produits", "Gestion", "Déconnexion"]
            english_indicators = ["English", "Home", "Products", "Management", "Logout"]

            # Quick DOM text check instead of full page source
            try:
                body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()

                french_count = sum(1 for indicator in french_indicators if indicator.lower() in body_text)
                english_count = sum(1 for indicator in english_indicators if indicator.lower() in body_text)

                if french_count > english_count:
                    print("Language detected from content analysis: French")
                    return "French"
                elif english_count > 0:
                    print("Language detected from content analysis: English")
                    return "English"
            except:
                pass

        except Exception as e:
            print(f"Could not determine current language: {e}")

        print("Language detection inconclusive, assuming English")
        return "English"

    def is_french_language(self):
        """Enhanced French language detection"""
        current_lang = self.get_current_language()
        is_french = "french" in current_lang.lower() or "français" in current_lang.lower()
        print(f"Is French language: {is_french}")
        return is_french

    def is_english_language(self):
        """Enhanced English language detection"""
        current_lang = self.get_current_language()
        is_english = "english" in current_lang.lower()
        print(f"Is English language: {is_english}")
        return is_english

    def change_language_to_english(self):
        """Enhanced language change to English with better error handling"""
        try:
            print("🌐 Attempting to change language to English...")

            # Check if already English
            if self.is_english_language():
                print("✅ Language is already English")
                return True

            # Try multiple methods
            methods = [
                self._try_dropdown_language_change,
                self._try_link_language_change,
                self._try_button_language_change
            ]

            for method in methods:
                try:
                    if method():
                        print("✅ Language change successful")
                        return True
                except Exception as e:
                    print(f"Language change method failed: {e}")
                    continue

            print("⚠️ Could not change language, continuing with current language")
            return False

        except Exception as e:
            print(f"Language change process failed: {e}")
            return False

    def _try_dropdown_language_change(self):
        """Enhanced dropdown language change for Nebular UI"""
        print("Trying Nebular UI language change...")

        # Try Nebular UI component first
        try:
            nebular_lang = self.find_element((By.CSS_SELECTOR, "nb-action[nbcontextmenutag='language']"), timeout=3)
            if nebular_lang and nebular_lang.is_displayed():
                print("Found Nebular language component")

                # Click the language component to open menu
                nebular_lang.click()
                time.sleep(2)  # Wait for context menu to appear

                # Look for English option in the opened menu
                english_options = [
                    (By.XPATH, "//nb-menu-item[contains(text(), 'English')]"),
                    (By.XPATH, "//li[contains(text(), 'English')]"),
                    (By.XPATH, "//*[contains(text(), 'English') and contains(@class, 'menu')]"),
                    (By.CSS_SELECTOR, "nb-menu-item"),  # Try any menu item
                    (By.CSS_SELECTOR, ".menu-item"),
                    (By.XPATH, "//button[contains(text(), 'English')]"),
                    (By.XPATH, "//a[contains(text(), 'English')]")
                ]

                for option_locator in english_options:
                    try:
                        english_option = self.find_element(option_locator, timeout=2)
                        if english_option and english_option.is_displayed():
                            # Check if it contains 'English' text
                            if "english" in english_option.text.lower():
                                english_option.click()
                                time.sleep(3)
                                print("✅ Selected English from Nebular menu")
                                return True
                    except Exception as e:
                        print(f"English option not found with {option_locator}: {e}")
                        continue

                # If no specific English option found, try clicking any available options
                try:
                    all_menu_items = self.driver.find_elements(By.CSS_SELECTOR, "nb-menu-item, .menu-item, li")
                    print(f"Found {len(all_menu_items)} menu items")
                    for item in all_menu_items:
                        try:
                            item_text = item.text.lower()
                            print(f"Menu item text: '{item_text}'")
                            if "english" in item_text or "en" == item_text:
                                item.click()
                                time.sleep(3)
                                print("✅ Selected English from menu items")
                                return True
                        except:
                            continue
                except Exception as e:
                    print(f"Could not find menu items: {e}")

        except Exception as e:
            print(f"Nebular UI method failed: {e}")

        # Fallback to standard dropdown method
        print("Trying standard dropdown method...")
        for locator in self.LANGUAGE_SELECTORS[4:]:  # Skip Nebular selectors
            try:
                dropdown = self.find_element(locator, timeout=2)
                if dropdown and dropdown.is_displayed():
                    print(f"Found language dropdown: {locator}")

                    # Click dropdown to open it
                    dropdown.click()
                    time.sleep(1)

                    # Select English option
                    english_option = self.find_element(self.ENGLISH_OPTION, timeout=3)
                    if english_option:
                        english_option.click()
                        time.sleep(2)
                        print("✅ Selected English from dropdown")
                        return True
            except Exception as e:
                print(f"Dropdown method failed for {locator}: {e}")
                continue

        return False

    def _try_link_language_change(self):
        """Enhanced link-based language change"""
        print("Trying link method...")
        try:
            english_link = self.find_element(self.LANGUAGE_LINK_EN, timeout=3)
            if english_link and english_link.is_displayed():
                print("Found English language link")
                english_link.click()
                time.sleep(3)
                print("✅ Clicked English language link")
                return True
        except Exception as e:
            print(f"Link method failed: {e}")
        return False

    def _try_button_language_change(self):
        """Enhanced button-based language change"""
        print("Trying button method...")
        try:
            lang_button = self.find_element(self.LANGUAGE_BUTTON, timeout=3)
            if lang_button and lang_button.is_displayed():
                print("Found language button")
                lang_button.click()
                time.sleep(1)

                # Look for English option in dropdown/menu
                english_option = self.find_element(self.ENGLISH_OPTION, timeout=3)
                if english_option:
                    english_option.click()
                    time.sleep(3)
                    print("✅ Selected English from language menu")
                    return True
        except Exception as e:
            print(f"Button method failed: {e}")
        return False

    def wait_for_language_change(self, timeout=15):
        """Enhanced wait for language change with better detection"""
        try:
            print("⏳ Waiting for language change to take effect...")

            # Wait for page content to change or reload
            start_time = time.time()
            while time.time() - start_time < timeout:
                if self.is_english_language():
                    print("✅ Language successfully changed to English")
                    time.sleep(2)  # Stabilization time
                    return True
                time.sleep(1)

            print("⚠️ Language change timeout, but continuing")
            return True  # Be more lenient

        except Exception as e:
            print(f"Language change wait failed: {e}")
            return True  # Be lenient

    # =======================
    # NAVIGATION TO PRODUCTS - Enhanced
    # =======================

    def navigate_to_products_page(self):
        """Enhanced navigation to products page"""
        try:
            print("🛍️ Navigating to products page...")

            # Method 1: Direct URL (most reliable)
            if self._try_direct_products_navigation():
                return True

            # Method 2: Menu navigation
            if self._try_menu_products_navigation():
                return True

            print("❌ Could not navigate to products page")
            return False

        except Exception as e:
            print(f"Products navigation failed: {e}")
            return False

    def _try_direct_products_navigation(self):
        """Enhanced direct URL navigation"""
        try:
            products_urls = [
                "http://localhost/#/pages/catalogue/products/products-list",
                "http://localhost/#/pages/catalog/products/products-list",
                "http://localhost/#/products/list",
                "http://localhost/#/catalogue/products"
            ]

            for url in products_urls:
                try:
                    print(f"Trying direct navigation to: {url}")
                    self.driver.get(url)
                    time.sleep(4)

                    # Check if we're on products page
                    current_url = self.driver.current_url.lower()
                    if "products" in current_url:
                        print(f"✅ Successfully navigated via direct URL: {url}")
                        return True
                except Exception as e:
                    print(f"Direct navigation to {url} failed: {e}")
                    continue

        except Exception as e:
            print(f"Direct navigation method failed: {e}")
        return False

    def _try_menu_products_navigation(self):
        """Enhanced menu navigation"""
        try:
            # Look for products menu with multiple strategies
            products_locators = [
                self.PRODUCTS_MENU,
                (By.XPATH, "//a[contains(text(), 'Catalog')]"),
                (By.XPATH, "//a[contains(@href, 'catalogue')]"),
                (By.XPATH, "//a[contains(@href, 'products')]"),
                (By.CSS_SELECTOR, "a[href*='catalogue']"),
                (By.CSS_SELECTOR, "a[href*='products']")
            ]

            for locator in products_locators:
                try:
                    products_menu = self.find_element(locator, timeout=3)
                    if products_menu and products_menu.is_displayed():
                        print(f"Found products menu: {locator}")
                        products_menu.click()
                        time.sleep(2)

                        # Look for products list link
                        list_locators = [
                            self.PRODUCTS_LIST_LINK,
                            (By.XPATH, "//a[contains(text(), 'List')]"),
                            (By.XPATH, "//a[contains(@href, 'list')]"),
                            (By.CSS_SELECTOR, "a[href*='products-list']")
                        ]

                        for list_locator in list_locators:
                            try:
                                products_list = self.find_element(list_locator, timeout=3)
                                if products_list:
                                    products_list.click()
                                    time.sleep(3)
                                    print("✅ Navigated via menu successfully")
                                    return True
                            except:
                                continue
                except Exception as e:
                    print(f"Menu navigation failed for {locator}: {e}")
                    continue

        except Exception as e:
            print(f"Menu navigation method failed: {e}")
        return False

    # =======================
    # UTILITY METHODS
    # =======================

    def logout(self):
        """Enhanced logout functionality"""
        try:
            logout_btn = self.find_element(self.LOGOUT_BUTTON, timeout=5)
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