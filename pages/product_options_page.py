from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
import time

class ProductOptionsPage(BasePage):
    """Page Object Model for Product Options/Property List Page"""

    # =======================
    # LOCATORS
    # =======================

    # Search/Filter Fields
    NAME_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Name']")
    MERCHANT_STORE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Merchant store']")
    MERCHANT_STORE_DROPDOWN = (By.CSS_SELECTOR, "button.ui-autocomplete-dropdown")

    # Table Headers (for sorting)
    ID_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.id a")
    NAME_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.descriptions a")
    TYPE_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.type a")

    # Table Content
    TABLE_ROWS = (By.CSS_SELECTOR, "ng2-smart-table tbody tr")
    TABLE_CELLS = (By.CSS_SELECTOR, "td")
    NO_DATA_MESSAGE = (By.CSS_SELECTOR, ".ng2-smart-no-data-message")

    # Buttons
    CREATE_OPTION_BTN = (By.CSS_SELECTOR, "a.createBtn")

    # Action Buttons
    UPDATE_BUTTONS = (By.CSS_SELECTOR, "a.ng2-smart-action-custom-custom i.nb-edit")
    DELETE_BUTTONS = (By.CSS_SELECTOR, "a.ng2-smart-action-custom-custom i.nb-trash")

    # Notification/Alert Messages
    NOTIFICATION = (By.CSS_SELECTOR, ".toast, .alert, .notification")

    # Pagination
    PAGINATION = (By.CSS_SELECTOR, ".pagination")
    PAGE_COUNTS = (By.CSS_SELECTOR, ".page-counts")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 15)

    # =======================
    # NAVIGATION METHOD
    # =======================

    def navigate_to_product_options_page(self):
        """Navigate directly to the product options page"""
        try:
            print("🔧 Navigating to product options page...")

            # Direct navigation to product options page
            self.driver.get("http://localhost/#/pages/catalogue/options/options-list")

            # Wait for page to load
            if self.wait_for_page_load():
                print("✓ Successfully navigated to product options page")
                return True

            print("❌ Failed to navigate to product options page")
            return False

        except Exception as e:
            print(f"Navigation failed: {str(e)}")
            return False

    def wait_for_page_load(self):
        """Wait for the product options page to fully load"""
        try:
            # Wait for key elements to be present
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located(self.NAME_SEARCH_INPUT),
                    EC.presence_of_element_located(self.CREATE_OPTION_BTN)
                )
            )

            # Additional wait for Angular to finish rendering
            time.sleep(2)

            print("✓ Product options page loaded successfully")
            return True

        except TimeoutException:
            print("❌ Product options page did not load within timeout")
            return False
        except Exception as e:
            print(f"❌ Page load verification failed: {str(e)}")
            return False

    # =======================
    # SEARCH/FILTER METHODS
    # =======================

    def enter_name_search(self, text):
        """Enter text in Name search field"""
        return self.enter_text(self.NAME_SEARCH_INPUT, text)

    def clear_name_search(self):
        """Clear Name search field"""
        element = self.find_element(self.NAME_SEARCH_INPUT)
        if element:
            element.clear()
            return True
        return False

    def get_name_search_value(self):
        """Get current value in Name search field"""
        element = self.find_element(self.NAME_SEARCH_INPUT)
        return element.get_attribute('value') if element else ""

    def click_merchant_store_dropdown(self):
        """Click merchant store dropdown"""
        return self.click_element(self.MERCHANT_STORE_DROPDOWN)

    def enter_merchant_store(self, text):
        """Enter text in merchant store field"""
        return self.enter_text(self.MERCHANT_STORE_INPUT, text)

    def get_merchant_store_value(self):
        """Get current value in merchant store field"""
        element = self.find_element(self.MERCHANT_STORE_INPUT)
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
            if len(cells) >= 4:  # Ensure we have enough columns (ID, Name, Type, Actions)
                row_data = {
                    'id': cells[0].text.strip(),
                    'name': cells[1].text.strip(),
                    'type': cells[2].text.strip(),
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
            'name': self.NAME_HEADER,
            'type': self.TYPE_HEADER
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
            'name': self.NAME_HEADER,
            'type': self.TYPE_HEADER
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

    def click_create_option(self):
        """Click Create Option/Property button"""
        return self.click_element(self.CREATE_OPTION_BTN)

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

    def search_and_verify_results(self, name_text=""):
        """Search with given criteria and return results"""
        if name_text:
            self.enter_name_search(name_text)

        self.wait_for_table_update()
        return self.get_table_data()

    def verify_search_results_contain_text(self, search_text, column='name'):
        """Verify that search results contain the expected text"""
        table_data = self.get_table_data()

        if not table_data:
            return False

        for row in table_data:
            if column in row and search_text.lower() in row[column].lower():
                return True

        return False

    def get_pagination_info(self):
        """Get pagination information"""
        try:
            page_counts = self.find_element(self.PAGE_COUNTS)
            return page_counts.text if page_counts else ""
        except:
            return ""

    def take_product_options_screenshot(self, filename="product_options_page"):
        """Take screenshot of product options page"""
        return self.take_screenshot(filename)