from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.home_page import HomePage
import time

class ProductsPage(BasePage):
    """Page Object Model for Products List Page with Authentication Support"""

    # =======================
    # LOCATORS
    # =======================

    # Search/Filter Fields
    SKU_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Sku']")
    PRODUCT_NAME_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Product name']")
    MERCHANT_DROPDOWN = (By.CSS_SELECTOR, "input[name='merchant']")
    MERCHANT_DROPDOWN_BUTTON = (By.CSS_SELECTOR, "button.ui-autocomplete-dropdown")

    # Table Headers (for sorting)
    ID_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.id a")
    SKU_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.sku a")
    PRODUCT_NAME_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.name a")
    QTY_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.quantity a")
    PRICE_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.price a")
    AVAILABLE_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.available a")
    CREATED_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.creationDate a")

    # Table Content
    TABLE_ROWS = (By.CSS_SELECTOR, "ng2-smart-table tbody tr")
    TABLE_CELLS = (By.CSS_SELECTOR, "td")
    NO_DATA_MESSAGE = (By.CSS_SELECTOR, ".ng2-smart-no-data-message")

    # Buttons
    CREATE_PRODUCT_BTN = (By.CSS_SELECTOR, "a.createBtn")

    # Available Toggle Checkboxes
    AVAILABLE_CHECKBOXES = (By.CSS_SELECTOR, "td input[type='checkbox']")

    # Notification/Alert Messages
    NOTIFICATION = (By.CSS_SELECTOR, ".toast, .alert, .notification")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 15)

    # =======================
    # AUTHENTICATION & NAVIGATION METHODS
    # =======================

    # def ensure_authenticated_and_navigate(self, base_url="http://localhost", force_login=False):
    #     """Ensure user is authenticated and navigate to products page"""
    #     try:
    #         print("\n" + "="*60)
    #         print("ENSURING AUTHENTICATION AND NAVIGATION")
    #         print("="*60)
    #
    #         # Check if we're already on the products page and authenticated
    #         if not force_login and self._is_on_products_page() and self._is_authenticated():
    #             print("✓ Already on products page and authenticated")
    #             return True
    #
    #         # Step 1: Handle login if needed
    #         if self._needs_login():
    #             print("Login required, performing authentication...")
    #             if not self._perform_full_authentication(base_url):
    #                 return False
    #
    #         # Step 2: Navigate to products page
    #         return self.navigate_to_products_page()
    #
    #     except Exception as e:
    #         print(f"❌ Authentication and navigation failed: {str(e)}")
    #         return False

    def _needs_login(self):
        """Check if login is needed"""
        current_url = self.driver.current_url.lower()

        # Check if we're on login page or if URL suggests we need to login
        if ("login" in current_url or
                current_url.endswith("/") or
                "localhost" == current_url.replace("http://", "").replace("https://", "")):
            return True

        # Check if we can access authenticated content
        try:
            # Try to find authenticated page elements
            authenticated_elements = [
                (By.CSS_SELECTOR, ".sidebar"),
                (By.CSS_SELECTOR, ".nav-sidebar"),
                (By.XPATH, "//a[contains(text(), 'Products') or contains(text(), 'Produits')]")
            ]

            for element in authenticated_elements:
                if self.is_element_visible(element, timeout=2):
                    return False

        except:
            pass

        return True

    def _is_authenticated(self):
        """Check if user is authenticated"""
        try:
            # Look for authenticated page indicators
            authenticated_indicators = [
                (By.CSS_SELECTOR, ".user-profile"),
                (By.CSS_SELECTOR, ".admin-user"),
                (By.XPATH, "//a[contains(text(), 'Logout')]"),
                (By.CSS_SELECTOR, ".sidebar")
            ]

            for indicator in authenticated_indicators:
                if self.is_element_visible(indicator, timeout=2):
                    return True

            return False

        except:
            return False

    def _is_on_products_page(self):
        """Check if currently on products page"""
        try:
            current_url = self.driver.current_url.lower()

            # Check URL
            if "products" in current_url and "list" in current_url:
                return True

            # Check for products page elements
            products_indicators = [
                self.SKU_SEARCH_INPUT,
                self.PRODUCT_NAME_SEARCH_INPUT,
                self.CREATE_PRODUCT_BTN
            ]

            for indicator in products_indicators:
                if self.is_element_visible(indicator, timeout=2):
                    return True

            return False

        except:
            return False

    def _perform_full_authentication(self, base_url):
        """Perform complete authentication flow"""
        try:
            # Step 1: Login
            login_page = LoginPage(self.driver)
            login_page.navigate_to_login_page(base_url)

            if not login_page.is_login_page_loaded():
                raise Exception("Login page did not load")

            login_success = login_page.perform_login(
                username="admin@shopizer.com",
                password="password"
            )

            if not login_success:
                raise Exception("Login failed")

            print("✓ Login successful")

            # Step 2: Handle language change
            home_page = HomePage(self.driver)
            home_page.wait_for_home_page_load()

            if home_page.is_french_language():
                print("Changing language to English...")
                if home_page.change_language_to_english():
                    home_page.wait_for_language_change()
                    print("✓ Language changed to English")
                else:
                    print("⚠ Could not change language")

            return True

        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            return False

    def navigate_to_products_page(self):
        """Navigate to the products list page"""
        try:
            print("Navigating to products page...")

            # Method 1: Try direct URL (fastest)
            self.driver.get("http://localhost/#/pages/catalogue/products/products-list")

            # Wait for page to load
            if self.wait_for_page_load():
                print("✓ Successfully navigated to products page")
                return True

            # Method 2: Try menu navigation as fallback
            print("Direct navigation failed, trying menu navigation...")
            home_page = HomePage(self.driver)
            if home_page.navigate_to_products_page():
                if self.wait_for_page_load():
                    print("✓ Successfully navigated via menu")
                    return True

            print("❌ Failed to navigate to products page")
            return False

        except Exception as e:
            print(f"Navigation failed: {str(e)}")
            return False

    def wait_for_page_load(self):
        """Wait for the products page to fully load"""
        try:
            # Wait for key elements to be present
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located(self.SKU_SEARCH_INPUT),
                    EC.presence_of_element_located(self.PRODUCT_NAME_SEARCH_INPUT)
                )
            )

            # Additional wait for Angular to finish rendering
            time.sleep(2)

            # Verify we're actually on the products page
            if self._is_on_products_page():
                return True
            else:
                raise Exception("Not on products page after navigation")

        except TimeoutException:
            print("Products page did not load within timeout")
            return False
        except Exception as e:
            print(f"Page load verification failed: {str(e)}")
            return False

    # =======================
    # SEARCH/FILTER METHODS
    # =======================

    def enter_sku_search(self, text):
        """Enter text in SKU search field"""
        return self.enter_text(self.SKU_SEARCH_INPUT, text)

    def enter_product_name_search(self, text):
        """Enter text in Product Name search field"""
        return self.enter_text(self.PRODUCT_NAME_SEARCH_INPUT, text)

    def clear_sku_search(self):
        """Clear SKU search field"""
        element = self.find_element(self.SKU_SEARCH_INPUT)
        if element:
            element.clear()
            return True
        return False

    def clear_product_name_search(self):
        """Clear Product Name search field"""
        element = self.find_element(self.PRODUCT_NAME_SEARCH_INPUT)
        if element:
            element.clear()
            return True
        return False

    def clear_all_search_fields(self):
        """Clear all search fields"""
        self.clear_sku_search()
        self.clear_product_name_search()
        time.sleep(1)  # Wait for table to refresh

    def get_sku_search_value(self):
        """Get current value in SKU search field"""
        element = self.find_element(self.SKU_SEARCH_INPUT)
        return element.get_attribute('value') if element else ""

    def get_product_name_search_value(self):
        """Get current value in Product Name search field"""
        element = self.find_element(self.PRODUCT_NAME_SEARCH_INPUT)
        return element.get_attribute('value') if element else ""

    # =======================
    # TABLE INTERACTION METHODS
    # =======================

    def get_table_rows(self):
        """Get all table rows"""
        return self.find_elements(self.TABLE_ROWS)

    def get_table_row_count(self):
        """Get number of visible table rows"""
        rows = self.get_table_rows()
        return len(rows)

    def is_table_empty(self):
        """Check if table shows no data"""
        try:
            # Check for no data message or empty table
            no_data = self.find_element(self.NO_DATA_MESSAGE, timeout=3)
            if no_data and no_data.is_displayed():
                return True

            # Alternative: check if table has no rows
            rows = self.get_table_rows()
            return len(rows) == 0

        except:
            rows = self.get_table_rows()
            return len(rows) == 0

    def get_table_data(self):
        """Get all table data as list of dictionaries"""
        rows = self.get_table_rows()
        table_data = []

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 7:  # Ensure we have enough columns
                row_data = {
                    'id': cells[0].text.strip(),
                    'sku': cells[1].text.strip(),
                    'product_name': cells[2].text.strip(),
                    'qty': cells[3].text.strip(),
                    'available': self._is_checkbox_checked(cells[4]),
                    'price': cells[5].text.strip(),
                    'created': cells[6].text.strip()
                }
                table_data.append(row_data)

        return table_data

    def _is_checkbox_checked(self, cell):
        """Check if checkbox in cell is checked"""
        try:
            checkbox = cell.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            return checkbox.is_selected()
        except:
            return False

    # =======================
    # SORTING METHODS
    # =======================

    def get_sort_order(self, header_locator):
        """Get current sort order of a column (asc, desc, or none)"""
        try:
            element = self.find_element(header_locator)
            if element:
                classes = element.get_attribute('class')
                if 'asc' in classes:
                    return 'asc'
                elif 'desc' in classes:
                    return 'desc'
                else:
                    return 'none'
        except:
            return 'none'

    def sort_by_column(self, column_name, order='asc'):
        """Sort by specific column with desired order"""
        header_map = {
            'id': self.ID_HEADER,
            'sku': self.SKU_HEADER,
            'product_name': self.PRODUCT_NAME_HEADER,
            'qty': self.QTY_HEADER,
            'price': self.PRICE_HEADER,
            'available': self.AVAILABLE_HEADER,
            'created': self.CREATED_HEADER
        }

        if column_name not in header_map:
            return False

        header_locator = header_map[column_name]
        current_order = self.get_sort_order(header_locator)

        if order == 'asc':
            if current_order != 'asc':
                self.click_element(header_locator)
                if self.get_sort_order(header_locator) != 'asc':
                    self.click_element(header_locator)  # Click again if needed
        elif order == 'desc':
            if current_order == 'none':
                self.click_element(header_locator)  # First click for asc
                time.sleep(0.5)
            if self.get_sort_order(header_locator) != 'desc':
                self.click_element(header_locator)  # Second click for desc

        time.sleep(1)  # Wait for sorting to complete
        return True

    # =======================
    # TOGGLE/CHECKBOX METHODS
    # =======================

    def click_available_toggle(self, row_index=0):
        """Click available toggle checkbox for specific row"""
        checkboxes = self.find_elements(self.AVAILABLE_CHECKBOXES)
        if row_index < len(checkboxes):
            checkboxes[row_index].click()
            time.sleep(0.5)  # Wait for potential notification
            return True
        return False

    def is_notification_displayed(self):
        """Check if notification is displayed after toggle action"""
        try:
            notification = self.find_element(self.NOTIFICATION, timeout=3)
            return notification and notification.is_displayed()
        except:
            return False

    # =======================
    # BUTTON ACTIONS
    # =======================

    def click_create_product(self):
        """Click Create Product button"""
        return self.click_element(self.CREATE_PRODUCT_BTN)

    # =======================
    # UTILITY METHODS
    # =======================

    def refresh_page(self):
        """Refresh the page to reset all filters and sorting"""
        self.driver.refresh()
        self.wait_for_page_load()

    def wait_for_table_update(self, timeout=5):
        """Wait for table to update after filter/sort action"""
        time.sleep(1)  # Basic wait for Angular table updates

    def search_and_verify_results(self, sku_text="", product_name_text=""):
        """Search with given criteria and return results"""
        if sku_text:
            self.enter_sku_search(sku_text)
        if product_name_text:
            self.enter_product_name_search(product_name_text)

        self.wait_for_table_update()
        return self.get_table_data()

    def verify_search_results_contain_text(self, search_text, column='sku'):
        """Verify that search results contain the expected text"""
        table_data = self.get_table_data()

        if not table_data:
            return False

        for row in table_data:
            if column in row and search_text.lower() in row[column].lower():
                return True

        return False

    def take_products_screenshot(self, filename="products_page"):
        """Take screenshot of products page"""
        return self.take_screenshot(filename)