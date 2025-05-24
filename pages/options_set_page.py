from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
import time

class OptionsSetPage(BasePage):
    """Page Object Model for Options Set / Property Set List Page"""

    # =======================
    # LOCATORS
    # =======================

    # Table Headers (for sorting)
    ID_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.id a")
    CODE_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.code a")
    OPTION_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.option a")
    VALUES_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.values a")
    PRODUCT_TYPES_HEADER = (By.CSS_SELECTOR, "th.ng2-smart-th.productTypes a")

    # Table Content
    TABLE_ROWS = (By.CSS_SELECTOR, "ng2-smart-table tbody tr")
    TABLE_CELLS = (By.CSS_SELECTOR, "td")
    NO_DATA_MESSAGE = (By.CSS_SELECTOR, ".ng2-smart-no-data-message")

    # Buttons
    CREATE_OPTIONS_SET_BTN = (By.CSS_SELECTOR, "a.createBtn")

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

    def navigate_to_options_set_page(self):
        """Navigate directly to the options set page"""
        try:
            print("⚙️ Navigating to options set page...")

            # Direct navigation to options set page
            self.driver.get("http://localhost/#/pages/catalogue/options/options-set-list")

            # Wait for page to load
            if self.wait_for_page_load():
                print("✓ Successfully navigated to options set page")
                return True

            print("❌ Failed to navigate to options set page")
            return False

        except Exception as e:
            print(f"Navigation failed: {str(e)}")
            return False

    def wait_for_page_load(self):
        """Wait for the options set page to fully load"""
        try:
            # Wait for key elements to be present
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located(self.CREATE_OPTIONS_SET_BTN),
                    EC.presence_of_element_located(self.ID_HEADER)
                )
            )

            # Additional wait for Angular to finish rendering
            time.sleep(2)

            print("✓ Options set page loaded successfully")
            return True

        except TimeoutException:
            print("❌ Options set page did not load within timeout")
            return False
        except Exception as e:
            print(f"❌ Page load verification failed: {str(e)}")
            return False

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
            if len(cells) >= 6:  # Ensure we have enough columns
                row_data = {
                    'id': cells[0].text.strip(),
                    'code': cells[1].text.strip(),
                    'option_name': cells[2].text.strip(),
                    'option_value': cells[3].text.strip(),
                    'product_types': cells[4].text.strip(),
                    'has_actions': self._has_action_buttons(cells[5])
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
            'code': self.CODE_HEADER,
            'option_name': self.OPTION_HEADER,
            'option_value': self.VALUES_HEADER,
            'product_types': self.PRODUCT_TYPES_HEADER
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
            'code': self.CODE_HEADER,
            'option_name': self.OPTION_HEADER,
            'option_value': self.VALUES_HEADER,
            'product_types': self.PRODUCT_TYPES_HEADER
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

    def get_column_data_for_verification(self, column_name):
        """Get data from specific column for sorting verification"""
        table_data = self.get_table_data()
        if not table_data:
            return []

        column_values = []
        for row in table_data:
            if column_name in row:
                value = row[column_name]
                # Convert to appropriate type for comparison
                if column_name == 'id':
                    try:
                        column_values.append(int(value))
                    except:
                        column_values.append(value)
                else:
                    column_values.append(value.lower() if value else '')

        return column_values

    def verify_sort_order(self, column_name, expected_order='asc'):
        """Verify if column is sorted in expected order"""
        column_data = self.get_column_data_for_verification(column_name)
        if len(column_data) <= 1:
            return True  # Single item or empty is always sorted

        if expected_order == 'asc':
            return column_data == sorted(column_data)
        elif expected_order == 'desc':
            return column_data == sorted(column_data, reverse=True)
        else:
            return True  # Can't verify 'none' order

    # =======================
    # BUTTON ACTIONS
    # =======================

    def click_create_options_set(self):
        """Click Create Options Set button"""
        return self.click_element(self.CREATE_OPTIONS_SET_BTN)

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
        """Wait for table to update after sort action"""
        time.sleep(1)  # Basic wait for Angular table updates

    def take_options_set_screenshot(self, filename="options_set_page"):
        """Take screenshot of options set page"""
        return self.take_screenshot(filename)

    def get_page_title(self):
        """Get the page title"""
        try:
            title_element = self.find_element((By.CSS_SELECTOR, "h1.page_title"))
            return title_element.text if title_element else ""
        except:
            return ""