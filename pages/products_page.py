from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
import time

class ProductsPage(BasePage):
    """Page Object Model for Products List Page"""

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
    # NAVIGATION METHODS
    # =======================

    def navigate_to_products_page(self):
        """Navigate to the products list page"""
        self.driver.get("http://localhost/#/pages/catalogue/products/products-list")
        self.wait_for_page_load()
        return self

    def wait_for_page_load(self):
        """Wait for the products page to fully load"""
        try:
            # Wait for the main table to be present
            self.wait.until(EC.presence_of_element_located(self.SKU_SEARCH_INPUT))
            # Small delay for Angular to finish rendering
            time.sleep(1)
        except TimeoutException:
            print("Products page did not load properly")

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

    def click_id_header(self):
        """Click ID column header for sorting"""
        return self.click_element(self.ID_HEADER)

    def click_sku_header(self):
        """Click SKU column header for sorting"""
        return self.click_element(self.SKU_HEADER)

    def click_product_name_header(self):
        """Click Product Name column header for sorting"""
        return self.click_element(self.PRODUCT_NAME_HEADER)

    def click_qty_header(self):
        """Click Quantity column header for sorting"""
        return self.click_element(self.QTY_HEADER)

    def click_price_header(self):
        """Click Price column header for sorting"""
        return self.click_element(self.PRICE_HEADER)

    def click_available_header(self):
        """Click Available column header for sorting"""
        return self.click_element(self.AVAILABLE_HEADER)

    def click_created_header(self):
        """Click Created column header for sorting"""
        return self.click_element(self.CREATED_HEADER)

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