from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
import time

class ProductTypesPage(BasePage):
    """Simplified Page Object Model for Product Types List Page"""

    # =======================
    # LOCATORS
    # =======================

    # Search/Filter Fields
    CODE_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Code']")
    MERCHANT_STORE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Merchant store']")
    MERCHANT_STORE_DROPDOWN = (By.CSS_SELECTOR, "button.ui-autocomplete-dropdown")

    # Table Headers (for sorting)
    ID_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.id a")
    MERCHANT_STORE_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.store a")
    CODE_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.code a")

    # Table Content
    TABLE_ROWS = (By.CSS_SELECTOR, "ng2-smart-table tbody tr")
    TABLE_CELLS = (By.CSS_SELECTOR, "td")
    NO_DATA_MESSAGE = (By.CSS_SELECTOR, ".ng2-smart-no-data-message")

    # Buttons
    CREATE_PRODUCT_TYPE_BTN = (By.CSS_SELECTOR, "a.createBtn")

    # Action Buttons
    UPDATE_BUTTONS = (By.CSS_SELECTOR, "a.ng2-smart-action-custom-custom i.nb-edit")
    DELETE_BUTTONS = (By.CSS_SELECTOR, "a.ng2-smart-action-custom-custom i.nb-trash")

    # Notification/Alert Messages
    NOTIFICATION = (By.CSS_SELECTOR, ".toast, .alert, .notification")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 15)

    # =======================
    # NAVIGATION METHOD
    # =======================

    def navigate_to_product_types_page(self):
        """Navigate directly to the product types page"""
        try:
            print("🏷️ Navigating to product types page...")

            # Direct navigation to product types page
            self.driver.get("http://localhost/#/pages/catalogue/types/types-list")

            # Wait for page to load
            if self.wait_for_page_load():
                print("✓ Successfully navigated to product types page")
                return True

            print("❌ Failed to navigate to product types page")
            return False

        except Exception as e:
            print(f"Navigation failed: {str(e)}")
            return False

    def wait_for_page_load(self):
        """Wait for the product types page to fully load"""
        try:
            # Wait for key elements to be present
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located(self.CODE_SEARCH_INPUT),
                    EC.presence_of_element_located(self.CREATE_PRODUCT_TYPE_BTN)
                )
            )

            # Additional wait for Angular to finish rendering
            time.sleep(2)

            print("✓ Product types page loaded successfully")
            return True

        except TimeoutException:
            print("❌ Product types page did not load within timeout")
            return False
        except Exception as e:
            print(f"❌ Page load verification failed: {str(e)}")
            return False

    # =======================
    # SEARCH/FILTER METHODS
    # =======================

    def enter_code_search(self, text):
        """Enter text in Code search field"""
        return self.enter_text(self.CODE_SEARCH_INPUT, text)

    def clear_code_search(self):
        """Clear Code search field"""
        element = self.find_element(self.CODE_SEARCH_INPUT)
        if element:
            element.clear()
            return True
        return False

    def get_code_search_value(self):
        """Get current value in Code search field"""
        element = self.find_element(self.CODE_SEARCH_INPUT)
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
            if len(cells) >= 4:  # Ensure we have enough columns (ID, Merchant Store, Code, Actions)
                row_data = {
                    'id': cells[0].text.strip(),
                    'merchant_store': cells[1].text.strip(),
                    'code': cells[2].text.strip(),
                    'has_actions': self._has_action_buttons(cells[3])
                }
                table_data.append(row_data)

        return table_data

    def _has_action_buttons(self, cell):
        """Check if action buttons are present in cell"""
        try:
            edit_btn = cell.find_element(By.CSS_SELECTOR, "i.nb-edit")
            delete_btn = cell.find_element(By.CSS_SELECTOR, "i.nb-trash")
            return edit_btn is not None and delete_btn is not None
        except:
            return False

    # =======================
    # SORTING METHODS (Simplified like product_groups)
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
            'merchant_store': self.MERCHANT_STORE_HEADER,
            'code': self.CODE_HEADER
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

    def click_sort_to_default(self, column_name):
        """Click column header until sorting returns to default (none)"""
        header_map = {
            'id': self.ID_HEADER,
            'merchant_store': self.MERCHANT_STORE_HEADER,
            'code': self.CODE_HEADER
        }

        if column_name not in header_map:
            return False

        header_locator = header_map[column_name]

        # Click up to 3 times to cycle through: none -> asc -> desc -> none
        for _ in range(3):
            current_order = self.get_sort_order(header_locator)
            if current_order == 'none':
                return True
            self.click_element(header_locator)
            time.sleep(0.5)

        return False

    # =======================
    # BUTTON ACTIONS
    # =======================

    def click_create_product_type(self):
        """Click Create Product Type button"""
        return self.click_element(self.CREATE_PRODUCT_TYPE_BTN)

    def click_update_button(self, row_index=0):
        """Click update button for specific row"""
        update_buttons = self.find_elements(self.UPDATE_BUTTONS)
        if row_index < len(update_buttons):
            update_buttons[row_index].click()
            return True
        return False

    def click_delete_button(self, row_index=0):
        """Click delete button for specific row"""
        delete_buttons = self.find_elements(self.DELETE_BUTTONS)
        if row_index < len(delete_buttons):
            delete_buttons[row_index].click()
            return True
        return False

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

    def search_and_verify_results(self, code_text=""):
        """Search with given criteria and return results"""
        if code_text:
            self.enter_code_search(code_text)

        self.wait_for_table_update()
        return self.get_table_data()

    def verify_search_results_contain_text(self, search_text, column='code'):
        """Verify that search results contain the expected text"""
        table_data = self.get_table_data()

        if not table_data:
            return False

        for row in table_data:
            if column in row and search_text.lower() in row[column].lower():
                return True

        return False

    def take_product_types_screenshot(self, filename="product_types_page"):
        """Take screenshot of product types page"""
        return self.take_screenshot(filename)