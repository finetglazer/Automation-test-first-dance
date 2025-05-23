import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime

class ProductTypesPage:
    """Page Object Model for Product Types page"""

    # URL
    PRODUCT_TYPES_URL = "http://localhost/#/pages/catalogue/types/types-list"

    # Locators
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(),'List of product types')]")

    # Table headers
    ID_HEADER = (By.XPATH, "//a[contains(text(),'ID')]")
    MERCHANT_STORE_HEADER = (By.XPATH, "//a[contains(text(),'Merchant store')]")
    CODE_HEADER = (By.XPATH, "//a[contains(text(),'Code')]")

    # Search/Filter inputs
    CODE_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Code']")
    MERCHANT_STORE_INPUT = (By.XPATH, "//input[@placeholder='Merchant store']")
    MERCHANT_STORE_DROPDOWN = (By.XPATH, "//button[contains(@class,'ui-autocomplete-dropdown')]")

    # Buttons
    CREATE_PRODUCT_TYPE_BTN = (By.XPATH, "//a[contains(@class,'createBtn')]")

    # Table
    TABLE = (By.XPATH, "//ng2-smart-table//table")
    TABLE_ROWS = (By.XPATH, "//tbody/tr")
    NO_DATA_MESSAGE = (By.XPATH, "//tbody//tr[contains(text(),'No data found')]")

    # Action buttons in table rows
    EDIT_BTN = (By.XPATH, "//i[contains(@class,'nb-edit')]")
    DELETE_BTN = (By.XPATH, "//i[contains(@class,'nb-trash')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_product_types_page(self):
        """Navigate to Product Types page"""
        self.driver.get(self.PRODUCT_TYPES_URL)
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """Wait for the page to fully load"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
            self.wait.until(EC.visibility_of_element_located(self.TABLE))
        except TimeoutException:
            raise TimeoutException("Product Types page failed to load within timeout period")

    def enter_code_search(self, text):
        """Enter text into Code search field"""
        search_input = self.wait.until(EC.element_to_be_clickable(self.CODE_SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(text)
        time.sleep(1)  # Allow time for filtering to apply

    def get_code_search_value(self):
        """Get current value in the code search field"""
        return self.driver.find_element(*self.CODE_SEARCH_INPUT).get_attribute('value')

    def select_merchant_store(self, store_name):
        """Select a merchant store from dropdown"""
        dropdown = self.wait.until(EC.element_to_be_clickable(self.MERCHANT_STORE_DROPDOWN))
        dropdown.click()
        store_option = (By.XPATH, f"//li[contains(text(),'{store_name}')]")
        self.wait.until(EC.element_to_be_clickable(store_option)).click()

    def sort_by_column(self, column, order='asc'):
        """Sort table by specified column and order"""
        header_map = {
            'id': self.ID_HEADER,
            'merchant_store': self.MERCHANT_STORE_HEADER,
            'code': self.CODE_HEADER
        }

        header = self.wait.until(EC.element_to_be_clickable(header_map[column]))

        # Check current sort state
        sort_state = self.get_sort_order(header_map[column])

        if order == 'asc' and sort_state != 'asc':
            # Click once for ascending or twice for descending->ascending
            header.click()
            if sort_state == 'desc':
                header.click()
        elif order == 'desc':
            if sort_state == 'none':
                # Click twice for none->ascending->descending
                header.click()
                time.sleep(0.5)
                header.click()
            elif sort_state == 'asc':
                # Click once for ascending->descending
                header.click()

        time.sleep(1)  # Wait for sort to apply

    def click_sort_to_default(self, column):
        """Click column header until sorting returns to default state"""
        header_map = {
            'id': self.ID_HEADER,
            'merchant_store': self.MERCHANT_STORE_HEADER,
            'code': self.CODE_HEADER
        }

        header = self.wait.until(EC.element_to_be_clickable(header_map[column]))

        # Click until sort indicator disappears (usually 3 clicks: none->asc->desc->none)
        max_clicks = 3
        for _ in range(max_clicks):
            if self.get_sort_order(header_map[column]) == 'none':
                break
            header.click()
            time.sleep(0.5)

    def get_sort_order(self, header_locator):
        """Get current sort order of a column: 'asc', 'desc', or 'none'"""
        header = self.driver.find_element(*header_locator)
        parent = header.find_element(By.XPATH, "./ancestor::ng2-smart-table-title")

        try:
            if parent.find_element(By.XPATH, "./a[contains(@class, 'asc')]"):
                return 'asc'
        except NoSuchElementException:
            pass

        try:
            if parent.find_element(By.XPATH, "./a[contains(@class, 'desc')]"):
                return 'desc'
        except NoSuchElementException:
            pass

        return 'none'

    def get_table_data(self):
        """Extract data from the table"""
        try:
            rows = self.driver.find_elements(*self.TABLE_ROWS)
            data = []

            for row in rows:
                # Check if this is a "No data" message row
                if 'No data found' in row.text:
                    return []

                cells = row.find_elements(By.XPATH, ".//td")
                if len(cells) >= 4:  # ID, Merchant store, Code, Actions
                    row_data = {
                        'id': cells[0].text.strip(),
                        'merchant_store': cells[1].text.strip(),
                        'code': cells[2].text.strip(),
                        'has_actions': len(cells[3].find_elements(By.TAG_NAME, "a")) > 0
                    }
                    data.append(row_data)

            return data
        except NoSuchElementException:
            return []

    def verify_search_results_contain_text(self, search_text, column='code'):
        """Verify all search results contain the search text in the specified column"""
        data = self.get_table_data()
        if not data:
            return False

        for row in data:
            if search_text.lower() not in row[column].lower():
                return False

        return True

    def wait_for_table_update(self):
        """Wait for the table to update after an action"""
        time.sleep(1)

    def refresh_page(self):
        """Refresh the page"""
        self.driver.refresh()
        self.wait_for_page_load()

    def is_element_visible(self, locator):
        """Check if an element is visible on the page"""
        try:
            return self.driver.find_element(*locator).is_displayed()
        except NoSuchElementException:
            return False

    def take_product_types_screenshot(self, name):
        """Take a screenshot with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/product_types_{name}_{timestamp}.png"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.driver.save_screenshot(filename)
        return filename