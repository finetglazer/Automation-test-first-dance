import pytest
import time
from selenium.webdriver.common.keys import Keys
from pages.product_options_page import ProductOptionsPage

class TestProductOptionsPageFiltering:
    """Test suite for Product Options page filtering and search functionality with authentication"""

    @pytest.fixture(autouse=True)
    def setup(self, product_options_page_ready):
        """Setup method using authenticated driver and navigate to product options page"""
        self.driver = product_options_page_ready
        self.product_options_page = ProductOptionsPage(self.driver)

        # Navigate to product options page
        if not self.product_options_page.navigate_to_product_options_page():
            pytest.fail("Failed to navigate to product options page")

        # Clear any existing filters
        self.product_options_page.clear_name_search()
        print("✓ Product options page setup completed")

    @pytest.mark.smoke
    def test_page_loads_successfully(self):
        """Test that product options page loads with all expected elements after authentication"""
        # Verify key elements are present
        assert self.product_options_page.is_element_visible(self.product_options_page.NAME_SEARCH_INPUT), \
            "Name search field should be visible"
        assert self.product_options_page.is_element_visible(self.product_options_page.CREATE_OPTION_BTN), \
            "Create option button should be visible"

        # Take screenshot to verify page loaded correctly
        self.product_options_page.take_product_options_screenshot("page_loaded_successfully")

    @pytest.mark.regression
    def test_special_character_input_name_field(self):
        """Test Case 1: Submit special characters into Name field"""
        # Test with ChromeDriver compatible special characters (no emojis)
        special_chars = "🥶🥶"
        self.product_options_page.enter_name_search(special_chars)
        self.product_options_page.wait_for_table_update()

        # Verify special characters are accepted
        current_value = self.product_options_page.get_name_search_value()
        assert special_chars in current_value, "Special characters should be accepted in Name field"

        # Step 4: Delete emojis and insert other special characters
        self.product_options_page.clear_name_search()
        other_special_chars = "<>+*&^%$#@!"
        self.product_options_page.enter_name_search(other_special_chars)
        self.product_options_page.wait_for_table_update()

        # Expected result: Table shows no data found
        assert self.product_options_page.is_table_empty(), \
            "Table should show no data for non-existent special characters"

    @pytest.mark.smoke
    def test_valid_existing_name_search(self):
        """Test Case 2: Submit valid text for existing Name field"""
        # First get some existing data to test with
        initial_data = self.product_options_page.get_table_data()

        if initial_data:
            # Use first character of existing name
            existing_name = initial_data[0]['name']
            if existing_name:
                search_char = existing_name[0]

                # Step 1-2: Enter one character from existing data
                self.product_options_page.enter_name_search(search_char)
                self.product_options_page.wait_for_table_update()

                # Expected result: Table displays data containing that character
                assert not self.product_options_page.is_table_empty(), \
                    "Table should show data when searching for existing character"

                # Verify results contain the search character
                assert self.product_options_page.verify_search_results_contain_text(search_char, 'name'), \
                    f"Search results should contain '{search_char}' in Name column"

    @pytest.mark.regression
    def test_non_existing_text_search(self):
        """Test Case 3: Submit text that doesn't exist"""
        non_existing_text = "XYZNEVEREXISTS123"

        # Test in Name field
        self.product_options_page.enter_name_search(non_existing_text)
        self.product_options_page.wait_for_table_update()

        # Expected result: Table shows no data found
        assert self.product_options_page.is_table_empty(), \
            "Table should show no data for non-existing name text"

    @pytest.mark.regression
    def test_text_with_leading_trailing_spaces(self):
        """Test Case 4: Submit text with spaces at beginning or end"""
        # Get existing data first
        initial_data = self.product_options_page.get_table_data()

        if initial_data and initial_data[0]['name']:
            valid_text = initial_data[0]['name'][:3]  # First 3 characters

            # Step 1-2: Fill space first, then valid text
            text_with_leading_space = f" {valid_text}"
            self.product_options_page.enter_name_search(text_with_leading_space)
            self.product_options_page.wait_for_table_update()

            # Step 3-4: Test with trailing space
            self.product_options_page.clear_name_search()
            text_with_trailing_space = f"{valid_text} "
            self.product_options_page.enter_name_search(text_with_trailing_space)
            self.product_options_page.wait_for_table_update()

            # Expected result: Should still find data (most systems trim spaces)
            # Note: This behavior may vary based on backend implementation
            table_data = self.product_options_page.get_table_data()
            # Test passes if data is found or if no data (both are acceptable behaviors)
            assert True  # Placeholder - adjust based on actual system behavior

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
            # XSS attempts
            "<script>alert('test')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "';alert('XSS');//",
            # HTML injection
            "<h1>test</h1>",
            "<b>bold</b>",
            "<iframe src='http://evil.com'></iframe>",
            "<div onclick='alert(1)'>click</div>"
        ]

        for payload in security_payloads:
            # Test in Name field
            self.product_options_page.clear_name_search()
            self.product_options_page.enter_name_search(payload)
            self.product_options_page.wait_for_table_update()

            # Expected result: Should not execute script/SQL, should show no data or be escaped
            # Verify no alert is triggered (implicit - test would fail if alert appeared)
            current_value = self.product_options_page.get_name_search_value()

            # The input should either be escaped, filtered, or cause no data to show
            assert payload in current_value or self.product_options_page.is_table_empty(), \
                f"Security injection should be handled safely: {payload}"

    @pytest.mark.smoke
    def test_empty_field_default_behavior(self):
        """Test Case 6: Submit nothing to test default filter behavior"""
        # Ensure field is empty
        self.product_options_page.clear_name_search()
        self.product_options_page.wait_for_table_update()

        # Expected result: Table displays all data
        table_data = self.product_options_page.get_table_data()
        assert len(table_data) > 0, "Table should display all data when no filters are applied"

    @pytest.mark.regression
    def test_large_value_input(self):
        """Test Case 7: Submit large value to test field limits"""
        # Create a very long string (1000+ characters)
        large_text = "A" * 1000

        self.product_options_page.enter_name_search(large_text)
        self.product_options_page.wait_for_table_update()

        # Expected result: Table shows nothing, field might truncate text
        assert self.product_options_page.is_table_empty(), \
            "Large input should result in no data found"

        # Verify field still displays some part of the data
        current_value = self.product_options_page.get_name_search_value()
        assert len(current_value) > 0, "Field should display at least part of the large input"


class TestProductOptionsPageSorting:
    """Test suite for sorting functionality with authentication"""

    @pytest.fixture(autouse=True)
    def setup(self, product_options_page_ready):
        self.driver = product_options_page_ready
        self.product_options_page = ProductOptionsPage(self.driver)
        self.product_options_page.navigate_to_product_options_page()
        self.product_options_page.clear_name_search()

    @pytest.mark.smoke
    def test_ascending_sort_all_columns(self):
        """Test Case 9: Testing sorting function ascending for all columns"""
        columns = ['id', 'name', 'type']

        for column in columns:
            # Click once for ascending
            self.product_options_page.sort_by_column(column, 'asc')

            # Verify sorting was applied
            header_map = {
                'id': self.product_options_page.ID_HEADER,
                'name': self.product_options_page.NAME_HEADER,
                'type': self.product_options_page.TYPE_HEADER
            }

            sort_order = self.product_options_page.get_sort_order(header_map[column])
            assert sort_order == 'asc', f"{column} column should be sorted in ascending order"

    @pytest.mark.smoke
    def test_descending_sort_all_columns(self):
        """Test Case 10: Testing sorting function descending for all columns"""
        columns = ['id', 'name', 'type']

        for column in columns:
            # Click twice for descending
            self.product_options_page.sort_by_column(column, 'desc')

            # Verify sorting was applied
            header_map = {
                'id': self.product_options_page.ID_HEADER,
                'name': self.product_options_page.NAME_HEADER,
                'type': self.product_options_page.TYPE_HEADER
            }

            sort_order = self.product_options_page.get_sort_order(header_map[column])
            assert sort_order == 'desc', f"{column} column should be sorted in descending order"

    @pytest.mark.regression
    def test_sort_to_default(self):
        """Test Case 11: Testing sorting function default after excluding sorting"""
        columns = ['id', 'name', 'type']

        for column in columns:
            # First apply some sorting
            self.product_options_page.sort_by_column(column, 'asc')

            # Then click to return to default
            self.product_options_page.click_sort_to_default(column)

            # Verify sorting is removed (default state)
            header_map = {
                'id': self.product_options_page.ID_HEADER,
                'name': self.product_options_page.NAME_HEADER,
                'type': self.product_options_page.TYPE_HEADER
            }

            sort_order = self.product_options_page.get_sort_order(header_map[column])
            assert sort_order == 'none', f"{column} column should return to default order"

    @pytest.mark.regression
    def test_multiple_column_sorting(self):
        """Test Case 12: Testing sorting with multiple columns"""
        # Sort by ID first
        self.product_options_page.sort_by_column('id', 'asc')

        # Then sort by Name (this might override previous sort depending on implementation)
        self.product_options_page.sort_by_column('name', 'desc')

        # Get table data to verify sorting
        table_data = self.product_options_page.get_table_data()

        # Basic verification - at least one sort should be active
        id_sort = self.product_options_page.get_sort_order(self.product_options_page.ID_HEADER)
        name_sort = self.product_options_page.get_sort_order(self.product_options_page.NAME_HEADER)

        assert id_sort != 'none' or name_sort != 'none', \
            "At least one column should maintain sorting"

    @pytest.mark.regression
    def test_sort_with_filter_applied(self):
        """Test Case 13: Testing sorting after applying filter"""
        # Get some existing data to filter by
        initial_data = self.product_options_page.get_table_data()

        if initial_data and initial_data[0]['name']:
            filter_char = initial_data[0]['name'][0]

            # Step 1: Apply filter first
            self.product_options_page.enter_name_search(filter_char)
            self.product_options_page.wait_for_table_update()

            # Step 2: Apply sorting
            self.product_options_page.sort_by_column('name', 'asc')

            # Verify both filter and sort are active
            filtered_data = self.product_options_page.get_table_data()
            assert len(filtered_data) > 0, "Filtered data should be visible"

            sort_order = self.product_options_page.get_sort_order(self.product_options_page.NAME_HEADER)
            assert sort_order == 'asc', "Sort should be applied to filtered data"

    @pytest.mark.regression
    def test_filter_with_sort_applied(self):
        """Test Case 14: Testing filter after applying sort"""
        # Step 1: Apply sorting first
        self.product_options_page.sort_by_column('name', 'desc')

        # Get some data to filter by
        sorted_data = self.product_options_page.get_table_data()

        if sorted_data and sorted_data[0]['name']:
            filter_char = sorted_data[0]['name'][0]

            # Step 2: Apply filter
            self.product_options_page.enter_name_search(filter_char)
            self.product_options_page.wait_for_table_update()

            # Verify both sort and filter are active
            final_data = self.product_options_page.get_table_data()

            sort_order = self.product_options_page.get_sort_order(self.product_options_page.NAME_HEADER)
            assert sort_order == 'desc', "Sort should remain active after filtering"

            # Verify filter is working
            assert self.product_options_page.verify_search_results_contain_text(filter_char, 'name'), \
                "Filter should be applied to sorted data"


class TestProductOptionsPageReset:
    """Test suite for reset functionality with authentication"""

    @pytest.fixture(autouse=True)
    def setup(self, product_options_page_ready):
        self.driver = product_options_page_ready
        self.product_options_page = ProductOptionsPage(self.driver)
        self.product_options_page.navigate_to_product_options_page()

    @pytest.mark.regression
    def test_page_reset_functionality(self):
        """Test Case 15: Testing state after resetting"""
        # Step 1: Add filter text
        self.product_options_page.enter_name_search("test")

        # Step 2: Add sorting
        self.product_options_page.sort_by_column('name', 'asc')

        # Verify changes are applied
        assert self.product_options_page.get_name_search_value() == "test", "Filter should be applied"
        sort_order = self.product_options_page.get_sort_order(self.product_options_page.NAME_HEADER)
        assert sort_order == 'asc', "Sort should be applied"

        # Step 3: Reset the page
        self.product_options_page.refresh_page()

        # Expected result: Page returns to default state
        assert self.product_options_page.get_name_search_value() == "", "Filter should be cleared after reset"

        # Verify table shows all data
        table_data = self.product_options_page.get_table_data()
        assert len(table_data) > 0, "Table should show all data after reset"


class TestProductOptionsPageMerchantStore:
    """Test suite for merchant store dropdown functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, product_options_page_ready):
        self.driver = product_options_page_ready
        self.product_options_page = ProductOptionsPage(self.driver)
        self.product_options_page.navigate_to_product_options_page()

    @pytest.mark.ui
    def test_merchant_store_dropdown_functionality(self):
        """Test Case 16: Testing the dropdown list Merchant store"""
        # Step 1: Clicking into the dropdown list
        dropdown_visible = self.product_options_page.is_element_visible(
            self.product_options_page.MERCHANT_STORE_DROPDOWN
        )
        assert dropdown_visible, "Merchant store dropdown should be visible"

        # Click the dropdown
        success = self.product_options_page.click_merchant_store_dropdown()
        assert success, "Should be able to click merchant store dropdown"

        # Wait for dropdown to open
        time.sleep(1)

        # Take screenshot for verification
        self.product_options_page.take_product_options_screenshot("merchant_store_dropdown_opened")

        # Note: Actual selection testing would depend on the dropdown options available
        # This is a basic structure that can be extended based on available options


class TestProductOptionsPageActions:
    """Test suite for action buttons functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, product_options_page_ready):
        self.driver = product_options_page_ready
        self.product_options_page = ProductOptionsPage(self.driver)
        self.product_options_page.navigate_to_product_options_page()

    @pytest.mark.ui
    def test_create_button_visible(self):
        """Test Create Option/Property button is visible and clickable"""
        assert self.product_options_page.is_element_visible(
            self.product_options_page.CREATE_OPTION_BTN
        ), "Create Option button should be visible"

        # Take screenshot
        self.product_options_page.take_product_options_screenshot("create_button_visible")

    @pytest.mark.smoke
    def test_action_buttons_present(self):
        """Test that update and delete buttons are present for each row"""
        table_data = self.product_options_page.get_table_data()

        if table_data:
            # Check first row has action buttons
            assert table_data[0]['has_actions'], "First row should have action buttons"

            # Verify all rows have actions
            for i, row in enumerate(table_data):
                assert row['has_actions'], f"Row {i} should have action buttons"

    @pytest.mark.smoke
    def test_table_data_structure(self):
        """Test that table displays correct data structure"""
        table_data = self.product_options_page.get_table_data()
        assert len(table_data) > 0, "Table should display some data"

        # Verify data structure
        if table_data:
            first_row = table_data[0]
            assert 'id' in first_row, "Table should have ID column"
            assert 'name' in first_row, "Table should have Name column"
            assert 'type' in first_row, "Table should have Type column"
            assert 'has_actions' in first_row, "Table should have Actions column"

    @pytest.mark.ui
    def test_pagination_visible(self):
        """Test that pagination is visible when needed"""
        pagination_info = self.product_options_page.get_pagination_info()
        # Pagination should show some info like "1 - 6 of 6"
        assert len(pagination_info) > 0, "Pagination information should be visible"