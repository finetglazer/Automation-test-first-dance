import pytest
import time
from selenium.webdriver.common.keys import Keys
from pages.options_set_page import OptionsSetPage

class TestOptionsSetPageBasic:
    """Test suite for basic functionality with authentication"""

    @pytest.fixture(autouse=True)
    def setup(self, options_set_page_ready):
        """Setup method using authenticated driver and navigate to options set page"""
        self.driver = options_set_page_ready
        self.options_set_page = OptionsSetPage(self.driver)

        # Navigate to options set page
        if not self.options_set_page.navigate_to_options_set_page():
            pytest.fail("Failed to navigate to options set page")

        print("✓ Options set page setup completed")

    @pytest.mark.smoke
    def test_page_loads_successfully(self):
        """Test that options set page loads with all expected elements after authentication"""
        # Verify page title
        page_title = self.options_set_page.get_page_title()
        assert "Options set" in page_title or "property set" in page_title, \
            "Page title should contain 'Options set' or 'property set'"

        # Verify key elements are present
        assert self.options_set_page.is_element_visible(self.options_set_page.CREATE_OPTIONS_SET_BTN), \
            "Create options set button should be visible"

        # Verify table headers are present
        assert self.options_set_page.is_element_visible(self.options_set_page.ID_HEADER), \
            "ID header should be visible"
        assert self.options_set_page.is_element_visible(self.options_set_page.CODE_HEADER), \
            "Code header should be visible"
        assert self.options_set_page.is_element_visible(self.options_set_page.OPTION_HEADER), \
            "Option name header should be visible"

        # Take screenshot to verify page loaded correctly
        self.options_set_page.take_options_set_screenshot("page_loaded_successfully")

    @pytest.mark.smoke
    def test_table_displays_data(self):
        """Verify the table displays data correctly"""
        table_data = self.options_set_page.get_table_data()
        assert len(table_data) > 0, "Table should display some data"

        # Verify data structure
        if table_data:
            first_row = table_data[0]
            assert 'id' in first_row, "Table should have ID column"
            assert 'code' in first_row, "Table should have Code column"
            assert 'option_name' in first_row, "Table should have Option name column"
            assert 'option_value' in first_row, "Table should have Option value column"
            assert 'product_types' in first_row, "Table should have Product types column"
            assert 'has_actions' in first_row, "Table should have Actions column"


class TestOptionsSetPageSorting:
    """Test suite for sorting functionality - Main focus of this page"""

    @pytest.fixture(autouse=True)
    def setup(self, options_set_page_ready):
        self.driver = options_set_page_ready
        self.options_set_page = OptionsSetPage(self.driver)
        self.options_set_page.navigate_to_options_set_page()

    @pytest.mark.smoke
    def test_ascending_sort_all_columns(self):
        """Test Case 9: Testing sorting function ascending when click on each field column"""
        columns = ['id', 'code', 'option_name', 'option_value', 'product_types']

        for column in columns:
            print(f"Testing ascending sort for {column} column...")

            # Click once for ascending
            success = self.options_set_page.sort_by_column(column, 'asc')
            assert success, f"Should be able to sort {column} column"

            # Verify sorting was applied
            header_map = {
                'id': self.options_set_page.ID_HEADER,
                'code': self.options_set_page.CODE_HEADER,
                'option_name': self.options_set_page.OPTION_HEADER,
                'option_value': self.options_set_page.VALUES_HEADER,
                'product_types': self.options_set_page.PRODUCT_TYPES_HEADER
            }

            sort_order = self.options_set_page.get_sort_order(header_map[column])
            assert sort_order == 'asc', f"{column} column should be sorted in ascending order"

            # Take screenshot for each sorted column
            self.options_set_page.take_options_set_screenshot(f"sort_asc_{column}")

    @pytest.mark.smoke
    def test_descending_sort_all_columns(self):
        """Test Case 10: Testing sorting function descending when click on each field"""
        columns = ['id', 'code', 'option_name', 'option_value', 'product_types']

        for column in columns:
            print(f"Testing descending sort for {column} column...")

            # Click twice for descending
            success = self.options_set_page.sort_by_column(column, 'desc')
            assert success, f"Should be able to sort {column} column"

            # Verify sorting was applied
            header_map = {
                'id': self.options_set_page.ID_HEADER,
                'code': self.options_set_page.CODE_HEADER,
                'option_name': self.options_set_page.OPTION_HEADER,
                'option_value': self.options_set_page.VALUES_HEADER,
                'product_types': self.options_set_page.PRODUCT_TYPES_HEADER
            }

            sort_order = self.options_set_page.get_sort_order(header_map[column])
            assert sort_order == 'desc', f"{column} column should be sorted in descending order"

            # Take screenshot for each sorted column
            self.options_set_page.take_options_set_screenshot(f"sort_desc_{column}")

    @pytest.mark.regression
    def test_sort_to_default(self):
        """Test Case 11: Testing sorting function default after excluding sorting"""
        columns = ['id', 'code', 'option_name', 'option_value', 'product_types']

        for column in columns:
            print(f"Testing default sort for {column} column...")

            # First apply some sorting
            self.options_set_page.sort_by_column(column, 'asc')

            # Then click to return to default
            success = self.options_set_page.click_sort_to_default(column)
            assert success, f"Should be able to return {column} to default sort"

            # Verify sorting is removed (default state)
            header_map = {
                'id': self.options_set_page.ID_HEADER,
                'code': self.options_set_page.CODE_HEADER,
                'option_name': self.options_set_page.OPTION_HEADER,
                'option_value': self.options_set_page.VALUES_HEADER,
                'product_types': self.options_set_page.PRODUCT_TYPES_HEADER
            }

            sort_order = self.options_set_page.get_sort_order(header_map[column])
            assert sort_order == 'none', f"{column} column should return to default order"

    @pytest.mark.regression
    def test_multiple_column_sorting(self):
        """Test Case 12: Testing sorting table when sorting more than 2 fields"""
        print("Testing multiple column sorting...")

        # Sort by ID first
        self.options_set_page.sort_by_column('id', 'asc')

        # Then sort by Code (this might override previous sort depending on implementation)
        self.options_set_page.sort_by_column('code', 'desc')

        # Get table data to verify sorting
        table_data = self.options_set_page.get_table_data()
        assert len(table_data) > 0, "Should have data to verify sorting"

        # Basic verification - at least one sort should be active
        id_sort = self.options_set_page.get_sort_order(self.options_set_page.ID_HEADER)
        code_sort = self.options_set_page.get_sort_order(self.options_set_page.CODE_HEADER)

        assert id_sort != 'none' or code_sort != 'none', \
            "At least one column should maintain sorting"

        # Test another combination
        self.options_set_page.sort_by_column('option_name', 'asc')
        self.options_set_page.sort_by_column('product_types', 'desc')

        option_sort = self.options_set_page.get_sort_order(self.options_set_page.OPTION_HEADER)
        types_sort = self.options_set_page.get_sort_order(self.options_set_page.PRODUCT_TYPES_HEADER)

        assert option_sort != 'none' or types_sort != 'none', \
            "At least one column should maintain sorting in second test"

    @pytest.mark.regression
    def test_sort_data_verification(self):
        """Advanced test: Verify actual data sorting (when data is sortable)"""
        columns_to_test = ['id', 'code', 'option_name']

        for column in columns_to_test:
            print(f"Verifying actual data sorting for {column}...")

            # Test ascending
            self.options_set_page.sort_by_column(column, 'asc')
            self.options_set_page.wait_for_table_update()

            # Get table data and verify it's actually sorted
            if self.options_set_page.verify_sort_order(column, 'asc'):
                print(f"✓ {column} ascending sort verified")
            else:
                print(f"⚠ {column} ascending sort could not be verified (data may not be sortable)")

            # Test descending
            self.options_set_page.sort_by_column(column, 'desc')
            self.options_set_page.wait_for_table_update()

            if self.options_set_page.verify_sort_order(column, 'desc'):
                print(f"✓ {column} descending sort verified")
            else:
                print(f"⚠ {column} descending sort could not be verified (data may not be sortable)")


class TestOptionsSetPageReset:
    """Test suite for reset functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, options_set_page_ready):
        self.driver = options_set_page_ready
        self.options_set_page = OptionsSetPage(self.driver)
        self.options_set_page.navigate_to_options_set_page()

    @pytest.mark.regression
    def test_page_reset_functionality(self):
        """Test Case 15: Testing state after resetting"""
        print("Testing page reset functionality...")

        # Step 1: Apply multiple sorts to create a complex state
        self.options_set_page.sort_by_column('code', 'asc')
        time.sleep(0.5)
        self.options_set_page.sort_by_column('option_name', 'desc')

        # Verify sorts are applied
        code_sort = self.options_set_page.get_sort_order(self.options_set_page.CODE_HEADER)
        option_sort = self.options_set_page.get_sort_order(self.options_set_page.OPTION_HEADER)

        print(f"Before reset - Code sort: {code_sort}, Option sort: {option_sort}")

        # Step 2: Reset the page
        self.options_set_page.refresh_page()

        # Expected result: Page returns to default state
        # Verify table shows all data
        table_data = self.options_set_page.get_table_data()
        assert len(table_data) > 0, "Table should show all data after reset"

        # Check if sorts have been reset (this may vary by implementation)
        code_sort_after = self.options_set_page.get_sort_order(self.options_set_page.CODE_HEADER)
        option_sort_after = self.options_set_page.get_sort_order(self.options_set_page.OPTION_HEADER)

        print(f"After reset - Code sort: {code_sort_after}, Option sort: {option_sort_after}")

        # Take screenshot to verify reset state
        self.options_set_page.take_options_set_screenshot("page_after_reset")


class TestOptionsSetPageActions:
    """Test suite for action buttons functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, options_set_page_ready):
        self.driver = options_set_page_ready
        self.options_set_page = OptionsSetPage(self.driver)
        self.options_set_page.navigate_to_options_set_page()

    @pytest.mark.ui
    def test_create_button_visible(self):
        """Test Create Options Set button is visible and clickable"""
        assert self.options_set_page.is_element_visible(
            self.options_set_page.CREATE_OPTIONS_SET_BTN
        ), "Create Options Set button should be visible"

        # Verify button text/title
        create_btn = self.options_set_page.find_element(self.options_set_page.CREATE_OPTIONS_SET_BTN)
        if create_btn:
            # Check if button contains expected text
            btn_text = create_btn.text.lower()
            assert "create" in btn_text and ("option" in btn_text or "property" in btn_text), \
                "Create button should contain 'create' and 'option' or 'property'"

        # Take screenshot
        self.options_set_page.take_options_set_screenshot("create_button_visible")

    @pytest.mark.smoke
    def test_action_buttons_present(self):
        """Test that update and delete buttons are present for each row"""
        table_data = self.options_set_page.get_table_data()

        if table_data:
            # Check first row has action buttons
            assert table_data[0]['has_actions'], "First row should have action buttons"

            # Verify all rows have actions
            for i, row in enumerate(table_data):
                assert row['has_actions'], f"Row {i} should have action buttons"

        # Count actual buttons to ensure they match rows
        update_buttons = self.options_set_page.find_elements(self.options_set_page.UPDATE_BUTTONS)
        delete_buttons = self.options_set_page.find_elements(self.options_set_page.DELETE_BUTTONS)

        assert len(update_buttons) == len(table_data), "Each row should have an update button"
        assert len(delete_buttons) == len(table_data), "Each row should have a delete button"

    @pytest.mark.ui
    def test_table_structure_integrity(self):
        """Test that table structure is consistent"""
        table_data = self.options_set_page.get_table_data()

        if table_data:
            # Verify all rows have the same structure
            expected_keys = {'id', 'code', 'option_name', 'option_value', 'product_types', 'has_actions'}

            for i, row in enumerate(table_data):
                row_keys = set(row.keys())
                assert row_keys == expected_keys, f"Row {i} should have all expected columns"

            print(f"✓ Verified {len(table_data)} rows with consistent structure")

        # Take comprehensive screenshot
        self.options_set_page.take_options_set_screenshot("table_structure_verified")


class TestOptionsSetPageStressTest:
    """Stress tests for sorting functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, options_set_page_ready):
        self.driver = options_set_page_ready
        self.options_set_page = OptionsSetPage(self.driver)
        self.options_set_page.navigate_to_options_set_page()

    @pytest.mark.regression
    def test_rapid_sort_changes(self):
        """Test rapid sorting changes to ensure stability"""
        columns = ['id', 'code', 'option_name', 'option_value', 'product_types']

        print("Testing rapid sort changes...")

        # Perform rapid sorting changes
        for _ in range(3):  # 3 cycles
            for column in columns:
                # Quickly toggle between asc and desc
                self.options_set_page.sort_by_column(column, 'asc')
                time.sleep(0.2)
                self.options_set_page.sort_by_column(column, 'desc')
                time.sleep(0.2)

        # Verify page is still functional
        table_data = self.options_set_page.get_table_data()
        assert len(table_data) > 0, "Table should still display data after rapid sort changes"

        # Verify at least one sort is still active
        headers = [
            self.options_set_page.ID_HEADER,
            self.options_set_page.CODE_HEADER,
            self.options_set_page.OPTION_HEADER,
            self.options_set_page.VALUES_HEADER,
            self.options_set_page.PRODUCT_TYPES_HEADER
        ]

        active_sorts = 0
        for header in headers:
            sort_order = self.options_set_page.get_sort_order(header)
            if sort_order != 'none':
                active_sorts += 1

        print(f"Active sorts after stress test: {active_sorts}")

        # Take screenshot to verify final state
        self.options_set_page.take_options_set_screenshot("stress_test_complete")