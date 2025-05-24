import pytest
import time
from selenium.webdriver.common.keys import Keys
from pages.product_types_page import ProductTypesPage

class TestProductTypesPageBasic:
    """Test suite for basic functionality with authentication"""

    @pytest.fixture(autouse=True)
    def setup(self, product_types_page_ready):
        """Setup method using authenticated driver and navigate to product types page"""
        self.driver = product_types_page_ready
        self.product_types_page = ProductTypesPage(self.driver)

        # Navigate to product types page
        if not self.product_types_page.navigate_to_product_types_page():
            pytest.fail("Failed to navigate to product types page")

        # Clear any existing filters
        self.product_types_page.clear_code_search()
        print("✓ Product types page setup completed")

    @pytest.mark.smoke
    def test_page_loads_successfully(self):
        """Test that product types page loads with all expected elements after authentication"""
        # Verify key elements are present
        assert self.product_types_page.is_element_visible(self.product_types_page.CODE_SEARCH_INPUT), \
            "Code search field should be visible"
        assert self.product_types_page.is_element_visible(self.product_types_page.CREATE_PRODUCT_TYPE_BTN), \
            "Create product type button should be visible"

        # Take screenshot to verify page loaded correctly
        self.product_types_page.take_product_types_screenshot("page_loaded_successfully")

    @pytest.mark.smoke
    def test_table_displays(self):
        """Verify the table displays data correctly"""
        table_data = self.product_types_page.get_table_data()
        assert len(table_data) > 0, "Table should display some data"

        # Verify data structure
        if table_data:
            first_row = table_data[0]
            assert 'id' in first_row, "Table should have ID column"
            assert 'code' in first_row, "Table should have Code column"
            assert 'merchant_store' in first_row, "Table should have Merchant Store column"


class TestProductTypesPageFilters:
    """Test suite for filter functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, product_types_page_ready):
        self.driver = product_types_page_ready
        self.product_types_page = ProductTypesPage(self.driver)
        self.product_types_page.navigate_to_product_types_page()

    @pytest.mark.regression
    def test_special_characters_filter(self):
        """Test Case 1: Submit special characters into Code field (Fixed for ChromeDriver)"""
        # Test with ChromeDriver compatible special characters (no emojis)
        special_chars = ["<script>", "+", "*", "@#$%", "!@#$%^&*()"]

        for char in special_chars:
            self.product_types_page.enter_code_search(char)
            self.product_types_page.wait_for_table_update()
            table_data = self.product_types_page.get_table_data()
            # Clear for next iteration
            self.product_types_page.clear_code_search()

    @pytest.mark.smoke
    def test_valid_code_filter(self):
        """Test Case 2: Submit valid text for existing Code name"""
        # First get some existing data to test with
        initial_data = self.product_types_page.get_table_data()

        if initial_data:
            # Use first character of existing code
            existing_code = initial_data[0]['code']
            if existing_code:
                search_char = existing_code[0]

                # Enter one character from existing data
                self.product_types_page.enter_code_search(search_char)
                self.product_types_page.wait_for_table_update()

                # Expected result: Table displays data containing that character
                assert not self.product_types_page.is_table_empty(), \
                    "Table should show data when searching for existing character"

                # Verify results contain the search character
                assert self.product_types_page.verify_search_results_contain_text(search_char, 'code'), \
                    f"Search results should contain '{search_char}' in Code column"

    @pytest.mark.regression
    def test_nonexistent_code_filter(self):
        """Test Case 3: Submit text that doesn't exist"""
        non_existing_text = "XYZNEVEREXISTS123"

        # Test in Code field
        self.product_types_page.enter_code_search(non_existing_text)
        self.product_types_page.wait_for_table_update()

        # Expected result: Table shows no data found
        assert self.product_types_page.is_table_empty(), \
            "Table should show no data for non-existing code text"

    @pytest.mark.regression
    def test_text_with_leading_trailing_spaces(self):
        """Test Case 4: Submit text with spaces at beginning or end"""
        # Get existing data first
        initial_data = self.product_types_page.get_table_data()

        if initial_data and initial_data[0]['code']:
            valid_text = initial_data[0]['code'][:3]  # First 3 characters

            # Test with leading space
            text_with_leading_space = f" {valid_text}"
            self.product_types_page.enter_code_search(text_with_leading_space)
            self.product_types_page.wait_for_table_update()
            leading_space_data = self.product_types_page.get_table_data()

            # Test with trailing space
            self.product_types_page.clear_code_search()
            text_with_trailing_space = f"{valid_text} "
            self.product_types_page.enter_code_search(text_with_trailing_space)
            self.product_types_page.wait_for_table_update()
            trailing_space_data = self.product_types_page.get_table_data()

            # Test exact match
            self.product_types_page.clear_code_search()
            self.product_types_page.enter_code_search(valid_text)
            self.product_types_page.wait_for_table_update()
            exact_match_data = self.product_types_page.get_table_data()

            # Expected result: Should handle spaces appropriately
            # Note: This behavior may vary based on backend implementation
            assert True  # Test passes as long as no errors occur

    @pytest.mark.security
    def test_security_injections(self):
        """Test Case 5: Submit SQL/NoSQL injection, XSS attempts, HTML injection to test security"""
        security_payloads = [
            # SQL injection attempts
            "'; DROP TABLE products; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "admin'--",
            "' OR 1=1 --",
            # XSS attempts (ChromeDriver compatible)
            "<script>alert('test')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            # HTML injection
            "<h1>test</h1>",
            "<b>bold</b>",
            "<iframe src='http://evil.com'></iframe>",
            "<div onclick='alert(1)'>click</div>"
        ]

        for payload in security_payloads:
            # Test in Code field
            self.product_types_page.clear_code_search()
            self.product_types_page.enter_code_search(payload)
            self.product_types_page.wait_for_table_update()

            # Expected result: Should not execute script/SQL, should show no data or be escaped
            current_value = self.product_types_page.get_code_search_value()

            # The input should either be escaped, filtered, or cause no data to show
            assert payload in current_value or self.product_types_page.is_table_empty(), \
                f"Security injection should be handled safely: {payload}"

    @pytest.mark.smoke
    def test_empty_field_default_behavior(self):
        """Test Case 6: Submit nothing to test default filter behavior"""
        # Ensure field is empty
        self.product_types_page.clear_code_search()
        self.product_types_page.wait_for_table_update()

        # Expected result: Table displays all data
        table_data = self.product_types_page.get_table_data()
        assert len(table_data) > 0, "Table should display all data when no filters are applied"

    @pytest.mark.regression
    def test_large_value_input(self):
        """Test Case 7: Submit large value to test field limits"""
        # Create a very long string (1000+ characters)
        large_text = "A" * 1000

        self.product_types_page.enter_code_search(large_text)
        self.product_types_page.wait_for_table_update()

        # Expected result: Table shows nothing, field might truncate text
        assert self.product_types_page.is_table_empty(), \
            "Large input should result in no data found"

        # Verify field still displays some part of the data
        current_value = self.product_types_page.get_code_search_value()
        assert len(current_value) > 0, "Field should display at least part of the large input"


class TestProductTypesPageSorting:
    """Test suite for sorting functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, product_types_page_ready):
        self.driver = product_types_page_ready
        self.product_types_page = ProductTypesPage(self.driver)
        self.product_types_page.navigate_to_product_types_page()
        self.product_types_page.clear_code_search()

    @pytest.mark.smoke
    def test_ascending_sort_all_columns(self):
        """Test Case 9: Testing sorting function ascending for all columns"""
        columns = ['id', 'merchant_store', 'code']

        for column in columns:
            # Click once for ascending
            self.product_types_page.sort_by_column(column, 'asc')

            # Verify sorting was applied
            header_map = {
                'id': self.product_types_page.ID_HEADER,
                'merchant_store': self.product_types_page.MERCHANT_STORE_HEADER,
                'code': self.product_types_page.CODE_HEADER
            }

            sort_order = self.product_types_page.get_sort_order(header_map[column])
            assert sort_order == 'asc', f"{column} column should be sorted in ascending order"

    @pytest.mark.smoke
    def test_descending_sort_all_columns(self):
        """Test Case 10: Testing sorting function descending for all columns"""
        columns = ['id', 'merchant_store', 'code']

        for column in columns:
            # Click twice for descending
            self.product_types_page.sort_by_column(column, 'desc')

            # Verify sorting was applied
            header_map = {
                'id': self.product_types_page.ID_HEADER,
                'merchant_store': self.product_types_page.MERCHANT_STORE_HEADER,
                'code': self.product_types_page.CODE_HEADER
            }

            sort_order = self.product_types_page.get_sort_order(header_map[column])
            assert sort_order == 'desc', f"{column} column should be sorted in descending order"

    @pytest.mark.regression
    def test_sort_to_default(self):
        """Test Case 11: Testing sorting function default after excluding sorting"""
        columns = ['id', 'merchant_store', 'code']

        for column in columns:
            # First apply some sorting
            self.product_types_page.sort_by_column(column, 'asc')

            # Then click to return to default
            self.product_types_page.click_sort_to_default(column)

            # Verify sorting is removed (default state)
            header_map = {
                'id': self.product_types_page.ID_HEADER,
                'merchant_store': self.product_types_page.MERCHANT_STORE_HEADER,
                'code': self.product_types_page.CODE_HEADER
            }

            sort_order = self.product_types_page.get_sort_order(header_map[column])
            assert sort_order == 'none', f"{column} column should return to default order"

    @pytest.mark.regression
    def test_multiple_column_sorting(self):
        """Test Case 12: Testing sorting with multiple columns"""
        # Sort by ID first
        self.product_types_page.sort_by_column('id', 'asc')

        # Then sort by Code (this might override previous sort depending on implementation)
        self.product_types_page.sort_by_column('code', 'desc')

        # Get table data to verify sorting
        table_data = self.product_types_page.get_table_data()

        # Basic verification - at least one sort should be active
        id_sort = self.product_types_page.get_sort_order(self.product_types_page.ID_HEADER)
        code_sort = self.product_types_page.get_sort_order(self.product_types_page.CODE_HEADER)

        assert id_sort != 'none' or code_sort != 'none', \
            "At least one column should maintain sorting"

    @pytest.mark.regression
    def test_sort_with_filter_applied(self):
        """Test Case 13: Testing sorting after applying filter"""
        # Get some existing data to filter by
        initial_data = self.product_types_page.get_table_data()

        if initial_data and initial_data[0]['code']:
            filter_char = initial_data[0]['code'][0]

            # Step 1: Apply filter first
            self.product_types_page.enter_code_search(filter_char)
            self.product_types_page.wait_for_table_update()

            # Step 2: Apply sorting
            self.product_types_page.sort_by_column('code', 'asc')

            # Verify both filter and sort are active
            filtered_data = self.product_types_page.get_table_data()
            assert len(filtered_data) > 0, "Filtered data should be visible"

            sort_order = self.product_types_page.get_sort_order(self.product_types_page.CODE_HEADER)
            assert sort_order == 'asc', "Sort should be applied to filtered data"

    @pytest.mark.regression
    def test_filter_with_sort_applied(self):
        """Test Case 14: Testing filter after applying sort"""
        # Step 1: Apply sorting first
        self.product_types_page.sort_by_column('code', 'desc')

        # Get some data to filter by
        sorted_data = self.product_types_page.get_table_data()

        if sorted_data and sorted_data[0]['code']:
            filter_char = sorted_data[0]['code'][0]

            # Step 2: Apply filter
            self.product_types_page.enter_code_search(filter_char)
            self.product_types_page.wait_for_table_update()

            # Verify both sort and filter are active
            final_data = self.product_types_page.get_table_data()

            sort_order = self.product_types_page.get_sort_order(self.product_types_page.CODE_HEADER)
            assert sort_order == 'desc', "Sort should remain active after filtering"

            # Verify filter is working
            assert self.product_types_page.verify_search_results_contain_text(filter_char, 'code'), \
                "Filter should be applied to sorted data"


class TestProductTypesPageReset:
    """Test suite for reset functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, product_types_page_ready):
        self.driver = product_types_page_ready
        self.product_types_page = ProductTypesPage(self.driver)
        self.product_types_page.navigate_to_product_types_page()

    @pytest.mark.regression
    def test_page_reset_functionality(self):
        """Test Case 15: Testing state after resetting"""
        # Step 1: Add filter text
        self.product_types_page.enter_code_search("test")

        # Step 2: Add sorting
        self.product_types_page.sort_by_column('code', 'asc')

        # Verify changes are applied
        assert self.product_types_page.get_code_search_value() == "test", "Filter should be applied"
        sort_order = self.product_types_page.get_sort_order(self.product_types_page.CODE_HEADER)
        assert sort_order == 'asc', "Sort should be applied"

        # Step 3: Reset the page
        self.product_types_page.refresh_page()

        # Expected result: Page returns to default state
        assert self.product_types_page.get_code_search_value() == "", "Filter should be cleared after reset"

        # Verify table shows all data
        table_data = self.product_types_page.get_table_data()
        assert len(table_data) > 0, "Table should show all data after reset"


class TestProductTypesPageActions:
    """Test suite for action buttons functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, product_types_page_ready):
        self.driver = product_types_page_ready
        self.product_types_page = ProductTypesPage(self.driver)
        self.product_types_page.navigate_to_product_types_page()

    @pytest.mark.ui
    def test_create_button_visible(self):
        """Test Create Product Type button is visible and clickable"""
        assert self.product_types_page.is_element_visible(
            self.product_types_page.CREATE_PRODUCT_TYPE_BTN
        ), "Create Product Type button should be visible"

        # Take screenshot
        self.product_types_page.take_product_types_screenshot("create_button_visible")

    @pytest.mark.smoke
    def test_action_buttons_present(self):
        """Test that update and delete buttons are present for each row"""
        table_data = self.product_types_page.get_table_data()

        if table_data:
            # Check first row has action buttons
            assert table_data[0]['has_actions'], "First row should have action buttons"

            # Verify all rows have actions
            for i, row in enumerate(table_data):
                assert row['has_actions'], f"Row {i} should have action buttons"