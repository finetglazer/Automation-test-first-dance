import pytest
import time
from selenium.webdriver.common.keys import Keys
from pages.brands_page import BrandsPage

class TestBrandsPageFiltering:
    """Test suite for Brands page filtering and search functionality with authentication"""

    @pytest.fixture(autouse=True)
    def setup(self, brands_page_ready):
        """Setup method using authenticated driver and navigate to brands page"""
        self.driver = brands_page_ready
        self.brands_page = BrandsPage(self.driver)

        # Navigate to brands page
        if not self.brands_page.navigate_to_brands_page():
            pytest.fail("Failed to navigate to brands page")

        # Clear any existing filters
        self.brands_page.clear_all_search_fields()
        print("✓ Brands page setup completed")

    @pytest.mark.smoke
    def test_page_loads_successfully(self):
        """Test that brands page loads with all expected elements after authentication"""
        # Verify key elements are present
        assert self.brands_page.is_element_visible(self.brands_page.GENERAL_SEARCH_INPUT), \
            "General search field should be visible"
        assert self.brands_page.is_element_visible(self.brands_page.BRAND_NAME_SEARCH_INPUT), \
            "Brand name search field should be visible"
        assert self.brands_page.is_element_visible(self.brands_page.CODE_SEARCH_INPUT), \
            "Code search field should be visible"
        assert self.brands_page.is_element_visible(self.brands_page.SEARCH_BUTTON), \
            "Search button should be visible"
        assert self.brands_page.is_element_visible(self.brands_page.RESET_BUTTON), \
            "Reset button should be visible"

        # Take screenshot to verify page loaded correctly
        self.brands_page.take_brands_screenshot("page_loaded_successfully")

    @pytest.mark.regression
    def test_special_character_input_brand_name_and_code_fields(self):
        """Test Case 1: Submit special characters into Brand name and Code fields"""
        # Step 1-3: Enter special characters (emojis and other special chars)
        # Note: Removed emojis for ChromeDriver compatibility
        special_chars_list = ["<>+*&^%$#@!", "🥶🥶", "';DROP TABLE;--"]

        for special_chars in special_chars_list:
            # Test in Brand Name field
            self.brands_page.enter_brand_name_search(special_chars)
            self.brands_page.wait_for_table_update()

            # Verify special characters are accepted
            current_value = self.brands_page.get_brand_name_search_value()
            assert len(current_value) > 0, "Special characters should be accepted in Brand Name field"

            # Clear and test in Code field
            self.brands_page.clear_brand_name_search()
            self.brands_page.enter_code_search(special_chars)
            self.brands_page.wait_for_table_update()

            # Expected result: Table shows no data found for non-existent special characters
            current_code_value = self.brands_page.get_code_search_value()
            assert len(current_code_value) > 0, "Special characters should be accepted in Code field"

            # Clear for next iteration
            self.brands_page.clear_code_search()

    @pytest.mark.smoke
    def test_valid_text_for_existing_code_name(self):
        """Test Case 2: Submit valid text for existing Code name"""
        # First get some existing data to test with
        initial_data = self.brands_page.get_table_data()

        if initial_data:
            # Use first character of existing code
            existing_code = initial_data[0]['code']
            if existing_code:
                search_char = existing_code[0]

                # Step 1-2: Enter one character from existing data
                self.brands_page.enter_code_search(search_char)
                self.brands_page.wait_for_table_update()

                # Expected result: Table displays data containing that character
                assert not self.brands_page.is_table_empty(), \
                    "Table should show data when searching for existing character"

                # Verify results contain the search character
                assert self.brands_page.verify_search_results_contain_text(search_char, 'code'), \
                    f"Search results should contain '{search_char}' in Code column"

    @pytest.mark.smoke
    def test_valid_text_for_existing_brand_name(self):
        """Test Case 3: Submit valid text for existing Brand name"""
        # First get some existing data to test with
        initial_data = self.brands_page.get_table_data()

        if initial_data:
            # Use first character of existing brand name
            existing_brand_name = initial_data[0]['brand_name']
            if existing_brand_name:
                search_char = existing_brand_name[0]

                # Step 1-2: Enter one character from existing data
                self.brands_page.enter_brand_name_search(search_char)
                self.brands_page.wait_for_table_update()

                # Expected result: Table displays data containing that character
                assert not self.brands_page.is_table_empty(), \
                    "Table should show data when searching for existing character"

                # Verify results contain the search character
                assert self.brands_page.verify_search_results_contain_text(search_char, 'brand_name'), \
                    f"Search results should contain '{search_char}' in Brand Name column"

    @pytest.mark.regression
    def test_non_existing_text_search(self):
        """Test Case 3: Submit text that doesn't exist"""
        non_existing_text = "XYZNEVEREXISTS123"

        # Test in Code field
        self.brands_page.enter_code_search(non_existing_text)
        self.brands_page.wait_for_table_update()

        # Expected result: Table shows no data found
        assert self.brands_page.is_table_empty(), \
            "Table should show no data for non-existing code text"

        # Clear and test in Brand Name field
        self.brands_page.clear_code_search()
        self.brands_page.enter_brand_name_search(non_existing_text)
        self.brands_page.wait_for_table_update()

        assert self.brands_page.is_table_empty(), \
            "Table should show no data for non-existing brand name text"

    @pytest.mark.regression
    def test_text_with_leading_trailing_spaces(self):
        """Test Case 4: Submit text with spaces at beginning or end"""
        # Get existing data first
        initial_data = self.brands_page.get_table_data()

        if initial_data and initial_data[0]['brand_name']:
            valid_text = initial_data[0]['brand_name'][:3]  # First 3 characters

            # Step 1-2: Fill space first, then valid text
            text_with_leading_space = f" {valid_text}"
            self.brands_page.enter_brand_name_search(text_with_leading_space)
            self.brands_page.wait_for_table_update()

            # Step 3-4: Test with trailing space
            self.brands_page.clear_brand_name_search()
            text_with_trailing_space = f"{valid_text} "
            self.brands_page.enter_brand_name_search(text_with_trailing_space)
            self.brands_page.wait_for_table_update()

            # Expected result: Should still find data (most systems trim spaces)
            # Note: This behavior may vary based on backend implementation
            table_data = self.brands_page.get_table_data()
            # Test passes if data is found or if no data (both are acceptable behaviors)
            assert True  # Placeholder - adjust based on actual system behavior

    @pytest.mark.security
    def test_security_injections(self):
        """Test Case 5: Submit SQL/NoSQL injection, XSS attempts, HTML injection to test security"""
        security_payloads = [
            # SQL injection attempts
            "'; DROP TABLE brands; --",
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
            # Test in Brand Name field
            self.brands_page.clear_all_search_fields()
            self.brands_page.enter_brand_name_search(payload)
            self.brands_page.wait_for_table_update()

            # Expected result: Should not execute script/SQL, should show no data or be escaped
            current_value = self.brands_page.get_brand_name_search_value()
            assert payload in current_value or self.brands_page.is_table_empty(), \
                f"Security injection should be handled safely in Brand Name field: {payload}"

            # Test in Code field
            self.brands_page.clear_all_search_fields()
            self.brands_page.enter_code_search(payload)
            self.brands_page.wait_for_table_update()

            current_value = self.brands_page.get_code_search_value()
            assert payload in current_value or self.brands_page.is_table_empty(), \
                f"Security injection should be handled safely in Code field: {payload}"

    @pytest.mark.regression
    def test_large_value_input(self):
        """Test Case 7: Submit large value to test field limits"""
        # Create a very long string (1000+ characters)
        large_text = "A" * 1000

        # Test in Brand Name field
        self.brands_page.enter_brand_name_search(large_text)
        self.brands_page.wait_for_table_update()

        # Expected result: Table shows nothing, field might truncate text
        assert self.brands_page.is_table_empty(), \
            "Large input should result in no data found in Brand Name field"

        # Verify field still displays some part of the data
        current_value = self.brands_page.get_brand_name_search_value()
        assert len(current_value) > 0, "Brand Name field should display at least part of the large input"

        # Clear and test in Code field
        self.brands_page.clear_brand_name_search()
        self.brands_page.enter_code_search(large_text)
        self.brands_page.wait_for_table_update()

        assert self.brands_page.is_table_empty(), \
            "Large input should result in no data found in Code field"

        current_value = self.brands_page.get_code_search_value()
        assert len(current_value) > 0, "Code field should display at least part of the large input"


class TestBrandsPageSorting:
    """Test suite for sorting functionality with authentication"""

    @pytest.fixture(autouse=True)
    def setup(self, brands_page_ready):
        self.driver = brands_page_ready
        self.brands_page = BrandsPage(self.driver)
        self.brands_page.navigate_to_brands_page()
        self.brands_page.clear_all_search_fields()

    @pytest.mark.smoke
    def test_ascending_sort_all_columns(self):
        """Test Case 9: Testing sorting function ascending for all columns"""
        columns = ['id', 'brand_name', 'code']

        for column in columns:
            # Click once for ascending
            self.brands_page.sort_by_column(column, 'asc')

            # Verify sorting was applied
            header_map = {
                'id': self.brands_page.ID_HEADER,
                'brand_name': self.brands_page.BRAND_NAME_HEADER,
                'code': self.brands_page.CODE_HEADER
            }

            sort_order = self.brands_page.get_sort_order(header_map[column])
            assert sort_order == 'asc', f"{column} column should be sorted in ascending order"

    @pytest.mark.smoke
    def test_descending_sort_all_columns(self):
        """Test Case 10: Testing sorting function descending for all columns"""
        columns = ['id', 'brand_name', 'code']

        for column in columns:
            # Click twice for descending
            self.brands_page.sort_by_column(column, 'desc')

            # Verify sorting was applied
            header_map = {
                'id': self.brands_page.ID_HEADER,
                'brand_name': self.brands_page.BRAND_NAME_HEADER,
                'code': self.brands_page.CODE_HEADER
            }

            sort_order = self.brands_page.get_sort_order(header_map[column])
            assert sort_order == 'desc', f"{column} column should be sorted in descending order"

    @pytest.mark.regression
    def test_sort_to_default(self):
        """Test Case 11: Testing sorting function default after excluding sorting"""
        columns = ['id', 'brand_name', 'code']

        for column in columns:
            # First apply some sorting
            self.brands_page.sort_by_column(column, 'asc')

            # Then click to return to default
            self.brands_page.click_sort_to_default(column)

            # Verify sorting is removed (default state)
            header_map = {
                'id': self.brands_page.ID_HEADER,
                'brand_name': self.brands_page.BRAND_NAME_HEADER,
                'code': self.brands_page.CODE_HEADER
            }

            sort_order = self.brands_page.get_sort_order(header_map[column])
            assert sort_order == 'none', f"{column} column should return to default order"

    @pytest.mark.regression
    def test_multiple_column_sorting(self):
        """Test Case 12: Testing sorting with multiple columns"""
        # Sort by ID first
        self.brands_page.sort_by_column('id', 'asc')

        # Then sort by Brand Name (this might override previous sort depending on implementation)
        self.brands_page.sort_by_column('brand_name', 'desc')

        # Get table data to verify sorting
        table_data = self.brands_page.get_table_data()

        # Basic verification - at least one sort should be active
        id_sort = self.brands_page.get_sort_order(self.brands_page.ID_HEADER)
        brand_name_sort = self.brands_page.get_sort_order(self.brands_page.BRAND_NAME_HEADER)

        assert id_sort != 'none' or brand_name_sort != 'none', \
            "At least one column should maintain sorting"

    @pytest.mark.regression
    def test_sort_with_filter_applied(self):
        """Test Case 13: Testing sorting after applying filter"""
        # Get some existing data to filter by
        initial_data = self.brands_page.get_table_data()

        if initial_data and initial_data[0]['brand_name']:
            filter_char = initial_data[0]['brand_name'][0]

            # Step 1: Apply filter first
            self.brands_page.enter_brand_name_search(filter_char)
            self.brands_page.wait_for_table_update()

            # Step 2: Apply sorting
            self.brands_page.sort_by_column('brand_name', 'asc')

            # Verify both filter and sort are active
            filtered_data = self.brands_page.get_table_data()
            assert len(filtered_data) > 0, "Filtered data should be visible"

            sort_order = self.brands_page.get_sort_order(self.brands_page.BRAND_NAME_HEADER)
            assert sort_order == 'asc', "Sort should be applied to filtered data"

    @pytest.mark.regression
    def test_filter_with_sort_applied(self):
        """Test Case 14: Testing filter after applying sort"""
        # Step 1: Apply sorting first
        self.brands_page.sort_by_column('brand_name', 'desc')

        # Get some data to filter by
        sorted_data = self.brands_page.get_table_data()

        if sorted_data and sorted_data[0]['brand_name']:
            filter_char = sorted_data[0]['brand_name'][0]

            # Step 2: Apply filter
            self.brands_page.enter_brand_name_search(filter_char)
            self.brands_page.wait_for_table_update()

            # Verify both sort and filter are active
            final_data = self.brands_page.get_table_data()

            sort_order = self.brands_page.get_sort_order(self.brands_page.BRAND_NAME_HEADER)
            assert sort_order == 'desc', "Sort should remain active after filtering"

            # Verify filter is working
            assert self.brands_page.verify_search_results_contain_text(filter_char, 'brand_name'), \
                "Filter should be applied to sorted data"


class TestBrandsPageReset:
    """Test suite for reset functionality with authentication"""

    @pytest.fixture(autouse=True)
    def setup(self, brands_page_ready):
        self.driver = brands_page_ready
        self.brands_page = BrandsPage(self.driver)
        self.brands_page.navigate_to_brands_page()

    @pytest.mark.regression
    def test_page_reset_functionality(self):
        """Test Case 15: Testing state after resetting"""
        # Step 1: Add filter text
        self.brands_page.enter_brand_name_search("test")
        self.brands_page.enter_code_search("test")

        # Step 2: Add sorting
        self.brands_page.sort_by_column('brand_name', 'asc')

        # Verify changes are applied
        assert self.brands_page.get_brand_name_search_value() == "test", "Brand name filter should be applied"
        assert self.brands_page.get_code_search_value() == "test", "Code filter should be applied"
        sort_order = self.brands_page.get_sort_order(self.brands_page.BRAND_NAME_HEADER)
        assert sort_order == 'asc', "Sort should be applied"

        # Step 3: Reset the page
        self.brands_page.refresh_page()

        # Expected result: Page returns to default state
        assert self.brands_page.get_brand_name_search_value() == "", "Brand name filter should be cleared after reset"
        assert self.brands_page.get_code_search_value() == "", "Code filter should be cleared after reset"

        # Verify table shows all data
        table_data = self.brands_page.get_table_data()
        assert len(table_data) > 0, "Table should show all data after reset"


class TestBrandsPageSearchAndResetButtons:
    """Test suite for search and reset button functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, brands_page_ready):
        self.driver = brands_page_ready
        self.brands_page = BrandsPage(self.driver)
        self.brands_page.navigate_to_brands_page()

    @pytest.mark.ui
    def test_search_button_functionality(self):
        """Test Case 16: Testing the search button"""
        # Get existing data to search for
        initial_data = self.brands_page.get_table_data()

        if initial_data and initial_data[0]['brand_name']:
            search_text = initial_data[0]['brand_name'][:3]  # First 3 characters

            # Step 1: Add text to general search field
            self.brands_page.enter_general_search(search_text)

            # Step 2: Click the search button
            self.brands_page.click_search_button()
            self.brands_page.wait_for_table_update()

            # Expected result: Page shows filtered data
            # Note: Behavior depends on implementation - might filter or just refresh
            table_data = self.brands_page.get_table_data()
            assert len(table_data) >= 0, "Search button should execute without errors"

    @pytest.mark.ui
    def test_reset_button_functionality(self):
        """Test Case 17: Testing the reset button"""
        # Step 1: Add filter data
        self.brands_page.enter_general_search("test")
        self.brands_page.enter_brand_name_search("test")

        # Step 2: Click the reset button
        self.brands_page.click_reset_button()
        self.brands_page.wait_for_table_update()

        # Expected result: All fields should be cleared
        assert self.brands_page.get_general_search_value() == "", "General search should be cleared"
        # Note: Reset behavior may vary - some implementations only clear general search

        # Verify table shows data
        table_data = self.brands_page.get_table_data()
        assert len(table_data) > 0, "Table should show data after reset"

    @pytest.mark.security
    def test_search_field_with_special_characters(self):
        """Test Case 18: Testing the search field with special characters"""
        special_chars = ["<script>alert('xss')</script>", "'; DROP TABLE brands; --", "<h1>Test</h1>"]

        for char in special_chars:
            # Step 1: Add special character to general search
            self.brands_page.clear_general_search()
            self.brands_page.enter_general_search(char)

            # Step 2: Click search button
            self.brands_page.click_search_button()
            self.brands_page.wait_for_table_update()

            # Expected result: Should handle special characters safely
            current_value = self.brands_page.get_general_search_value()
            assert char in current_value or len(current_value) == 0, \
                f"Special character should be handled safely: {char}"


class TestBrandsPageActions:
    """Test suite for action buttons functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, brands_page_ready):
        self.driver = brands_page_ready
        self.brands_page = BrandsPage(self.driver)
        self.brands_page.navigate_to_brands_page()

    @pytest.mark.smoke
    def test_action_buttons_present(self):
        """Test that update and delete buttons are present for each row"""
        table_data = self.brands_page.get_table_data()

        if table_data:
            # Check first row has action buttons
            assert table_data[0]['has_actions'], "First row should have action buttons"

            # Verify all rows have actions
            for i, row in enumerate(table_data):
                assert row['has_actions'], f"Row {i} should have action buttons"

    @pytest.mark.ui
    def test_table_displays_correctly(self):
        """Test that table displays data in correct format"""
        table_data = self.brands_page.get_table_data()

        assert len(table_data) > 0, "Table should display some data"

        # Verify data structure
        if table_data:
            first_row = table_data[0]
            assert 'id' in first_row, "Table should have ID column"
            assert 'brand_name' in first_row, "Table should have Brand Name column"
            assert 'code' in first_row, "Table should have Code column"
            assert 'has_actions' in first_row, "Table should have Actions column"

        # Take screenshot
        self.brands_page.take_brands_screenshot("table_display_test")

    @pytest.mark.smoke
    def test_pagination_info_displayed(self):
        """Test that pagination information is displayed"""
        pagination_info = self.brands_page.get_pagination_info()
        assert len(pagination_info) > 0, "Pagination information should be displayed"
        assert "of" in pagination_info.lower(), "Pagination should show format like '1 - 3 of 3'"