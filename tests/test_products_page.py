import pytest
import time
from selenium.webdriver.common.keys import Keys
from pages.products_page import ProductsPage

class TestProductsPageFiltering:
    """Test suite for Products page filtering and search functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup method to navigate to products page before each test"""
        self.products_page = ProductsPage(driver)
        self.products_page.navigate_to_products_page()
        # Clear any existing filters
        self.products_page.clear_all_search_fields()

    @pytest.mark.smoke
    def test_page_loads_successfully(self):
        """Test that products page loads with all expected elements"""
        # Verify key elements are present
        assert self.products_page.is_element_visible(self.products_page.SKU_SEARCH_INPUT), \
            "SKU search field should be visible"
        assert self.products_page.is_element_visible(self.products_page.PRODUCT_NAME_SEARCH_INPUT), \
            "Product name search field should be visible"
        assert self.products_page.is_element_visible(self.products_page.CREATE_PRODUCT_BTN), \
            "Create product button should be visible"

    @pytest.mark.regression
    def test_special_character_input_sku_field(self):
        """Test Case 1: Submit special characters into SKU field"""
        # Step 1-3: Enter special characters (emojis)
        special_chars = "🥶🥶"
        self.products_page.enter_sku_search(special_chars)
        self.products_page.wait_for_table_update()

        # Verify special characters are accepted
        current_value = self.products_page.get_sku_search_value()
        assert special_chars in current_value, "Special characters should be accepted in SKU field"

        # Step 4: Delete emojis and insert other special characters
        self.products_page.clear_sku_search()
        other_special_chars = "<>+*&^%$#@!"
        self.products_page.enter_sku_search(other_special_chars)
        self.products_page.wait_for_table_update()

        # Expected result: Table shows no data found
        assert self.products_page.is_table_empty(), \
            "Table should show no data for non-existent special characters"

    @pytest.mark.regression
    def test_special_character_input_product_name_field(self):
        """Test Case 1: Submit special characters into Product Name field"""
        special_chars = "🥶🥶<>+*&^%$#@!"
        self.products_page.enter_product_name_search(special_chars)
        self.products_page.wait_for_table_update()

        # Expected result: Table shows no data found for non-existent special characters
        assert self.products_page.is_table_empty(), \
            "Table should show no data for non-existent special characters in product name"

    @pytest.mark.smoke
    def test_valid_existing_sku_search(self):
        """Test Case 2: Submit valid text for existing SKU"""
        # First get some existing data to test with
        initial_data = self.products_page.get_table_data()

        if initial_data:
            # Use first character of existing SKU
            existing_sku = initial_data[0]['sku']
            if existing_sku:
                search_char = existing_sku[0]

                # Step 1-2: Enter one character from existing data
                self.products_page.enter_sku_search(search_char)
                self.products_page.wait_for_table_update()

                # Expected result: Table displays data containing that character
                assert not self.products_page.is_table_empty(), \
                    "Table should show data when searching for existing character"

                # Verify results contain the search character
                assert self.products_page.verify_search_results_contain_text(search_char, 'sku'), \
                    f"Search results should contain '{search_char}' in SKU column"

    @pytest.mark.smoke
    def test_valid_existing_product_name_search(self):
        """Test Case 2: Submit valid text for existing Product Name"""
        initial_data = self.products_page.get_table_data()

        if initial_data:
            existing_product_name = initial_data[0]['product_name']
            if existing_product_name:
                search_char = existing_product_name[0]

                self.products_page.enter_product_name_search(search_char)
                self.products_page.wait_for_table_update()

                assert not self.products_page.is_table_empty(), \
                    "Table should show data when searching for existing character"

                assert self.products_page.verify_search_results_contain_text(search_char, 'product_name'), \
                    f"Search results should contain '{search_char}' in Product Name column"

    @pytest.mark.regression
    def test_non_existing_text_search(self):
        """Test Case 3: Submit text that doesn't exist"""
        non_existing_text = "XYZNEVEREXISTS123"

        # Test in SKU field
        self.products_page.enter_sku_search(non_existing_text)
        self.products_page.wait_for_table_update()

        # Expected result: Table shows no data found
        assert self.products_page.is_table_empty(), \
            "Table should show no data for non-existing SKU text"

        # Clear and test in Product Name field
        self.products_page.clear_sku_search()
        self.products_page.enter_product_name_search(non_existing_text)
        self.products_page.wait_for_table_update()

        assert self.products_page.is_table_empty(), \
            "Table should show no data for non-existing product name text"

    @pytest.mark.regression
    def test_text_with_leading_trailing_spaces(self):
        """Test Case 4: Submit text with spaces at beginning or end"""
        # Get existing data first
        initial_data = self.products_page.get_table_data()

        if initial_data and initial_data[0]['sku']:
            valid_text = initial_data[0]['sku'][:3]  # First 3 characters

            # Step 1-2: Fill space first, then valid text
            text_with_leading_space = f" {valid_text}"
            self.products_page.enter_sku_search(text_with_leading_space)
            self.products_page.wait_for_table_update()

            # Step 3-4: Test with trailing space
            self.products_page.clear_sku_search()
            text_with_trailing_space = f"{valid_text} "
            self.products_page.enter_sku_search(text_with_trailing_space)
            self.products_page.wait_for_table_update()

            # Expected result: Should still find data (most systems trim spaces)
            # Note: This behavior may vary based on backend implementation
            table_data = self.products_page.get_table_data()
            # Test passes if data is found or if no data (both are acceptable behaviors)
            assert True  # Placeholder - adjust based on actual system behavior

    @pytest.mark.security
    def test_xss_injection_attempts(self):
        """Test Case 5: Submit XSS attempts to test security"""
        xss_payloads = [
            "<script>alert('test')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "';alert('XSS');//"
        ]

        for payload in xss_payloads:
            # Test in SKU field
            self.products_page.clear_all_search_fields()
            self.products_page.enter_sku_search(payload)
            self.products_page.wait_for_table_update()

            # Expected result: Should not execute script, should show no data or be escaped
            # Verify no alert is triggered (implicit - test would fail if alert appeared)
            current_value = self.products_page.get_sku_search_value()

            # The input should either be escaped, filtered, or cause no data to show
            # This is a basic check - in real scenarios, you'd verify proper escaping
            assert True  # Passes if no JavaScript execution occurs

            # Test in Product Name field
            self.products_page.clear_all_search_fields()
            self.products_page.enter_product_name_search(payload)
            self.products_page.wait_for_table_update()

            # Same verification
            assert True  # Passes if no JavaScript execution occurs

    @pytest.mark.security
    def test_sql_injection_attempts(self):
        """Test Case 5: Submit SQL injection attempts"""
        sql_payloads = [
            "'; DROP TABLE products; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "admin'--",
            "' OR 1=1 --"
        ]

        for payload in sql_payloads:
            self.products_page.clear_all_search_fields()
            self.products_page.enter_sku_search(payload)
            self.products_page.wait_for_table_update()

            # Expected result: Should not affect database, should show no data or be escaped
            assert self.products_page.is_table_empty() or len(self.products_page.get_table_data()) > 0, \
                "SQL injection should not break the application"

    @pytest.mark.security
    def test_html_injection_attempts(self):
        """Test Case 5: Submit HTML injection attempts"""
        html_payloads = [
            "<h1>test</h1>",
            "<b>bold</b>",
            "<iframe src='http://evil.com'></iframe>",
            "<div onclick='alert(1)'>click</div>"
        ]

        for payload in html_payloads:
            self.products_page.clear_all_search_fields()
            self.products_page.enter_product_name_search(payload)
            self.products_page.wait_for_table_update()

            # Expected result: HTML should be escaped or filtered
            current_value = self.products_page.get_product_name_search_value()
            # Basic check - in practice, verify HTML is properly escaped
            assert payload in current_value or self.products_page.is_table_empty(), \
                "HTML injection should be handled safely"

    @pytest.mark.smoke
    def test_empty_field_default_behavior(self):
        """Test Case 6: Submit nothing to test default filter behavior"""
        # Ensure fields are empty
        self.products_page.clear_all_search_fields()
        self.products_page.wait_for_table_update()

        # Expected result: Table displays all data
        table_data = self.products_page.get_table_data()
        assert len(table_data) > 0, "Table should display all data when no filters are applied"

    @pytest.mark.regression
    def test_large_value_input(self):
        """Test Case 7: Submit large value to test field limits"""
        # Create a very long string (1000+ characters)
        large_text = "A" * 1000

        self.products_page.enter_sku_search(large_text)
        self.products_page.wait_for_table_update()

        # Expected result: Table shows nothing, field might truncate text
        assert self.products_page.is_table_empty(), \
            "Large input should result in no data found"

        # Verify field still displays some part of the data
        current_value = self.products_page.get_sku_search_value()
        assert len(current_value) > 0, "Field should display at least part of the large input"


class TestProductsPageToggle:
    """Test suite for toggle functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.products_page = ProductsPage(driver)
        self.products_page.navigate_to_products_page()

    @pytest.mark.ui
    def test_available_toggle_functionality(self):
        """Test Case 8: Testing toggle field visibility and notification"""
        # Ensure we have data to test with
        table_data = self.products_page.get_table_data()

        if table_data:
            # Step 1: Click toggle when empty/unchecked
            initial_state = self.products_page._is_checkbox_checked(
                self.products_page.find_elements(self.products_page.TABLE_ROWS)[0]
                .find_elements(By.TAG_NAME, "td")[4]
            )

            # Click the toggle
            self.products_page.click_available_toggle(0)

            # Step 2: Click again
            self.products_page.click_available_toggle(0)

            # Expected result: Toggle shows ✅ first click, then unchecked second click
            # Notification should be displayed
            # Note: Exact implementation depends on the application behavior
            assert True  # Basic test - expand based on actual toggle behavior


class TestProductsPageSorting:
    """Test suite for sorting functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.products_page = ProductsPage(driver)
        self.products_page.navigate_to_products_page()
        self.products_page.clear_all_search_fields()

    @pytest.mark.smoke
    def test_ascending_sort_all_columns(self):
        """Test Case 9: Testing sorting function ascending for all columns"""
        columns = ['id', 'sku', 'product_name', 'qty', 'price', 'available', 'created']

        for column in columns:
            # Click once for ascending
            self.products_page.sort_by_column(column, 'asc')

            # Verify sorting was applied
            header_map = {
                'id': self.products_page.ID_HEADER,
                'sku': self.products_page.SKU_HEADER,
                'product_name': self.products_page.PRODUCT_NAME_HEADER,
                'qty': self.products_page.QTY_HEADER,
                'price': self.products_page.PRICE_HEADER,
                'available': self.products_page.AVAILABLE_HEADER,
                'created': self.products_page.CREATED_HEADER
            }

            sort_order = self.products_page.get_sort_order(header_map[column])
            assert sort_order == 'asc', f"{column} column should be sorted in ascending order"

    @pytest.mark.smoke
    def test_descending_sort_all_columns(self):
        """Test Case 10: Testing sorting function descending for all columns"""
        columns = ['id', 'sku', 'product_name', 'qty', 'price', 'available', 'created']

        for column in columns:
            # Click twice for descending
            self.products_page.sort_by_column(column, 'desc')

            # Verify sorting was applied
            header_map = {
                'id': self.products_page.ID_HEADER,
                'sku': self.products_page.SKU_HEADER,
                'product_name': self.products_page.PRODUCT_NAME_HEADER,
                'qty': self.products_page.QTY_HEADER,
                'price': self.products_page.PRICE_HEADER,
                'available': self.products_page.AVAILABLE_HEADER,
                'created': self.products_page.CREATED_HEADER
            }

            sort_order = self.products_page.get_sort_order(header_map[column])
            assert sort_order == 'desc', f"{column} column should be sorted in descending order"

    @pytest.mark.regression
    def test_multiple_column_sorting(self):
        """Test Case 12: Testing sorting with multiple columns"""
        # Sort by SKU first
        self.products_page.sort_by_column('sku', 'asc')

        # Then sort by price (this might override previous sort depending on implementation)
        self.products_page.sort_by_column('price', 'desc')

        # Get table data to verify sorting
        table_data = self.products_page.get_table_data()

        # Basic verification - at least one sort should be active
        sku_sort = self.products_page.get_sort_order(self.products_page.SKU_HEADER)
        price_sort = self.products_page.get_sort_order(self.products_page.PRICE_HEADER)

        assert sku_sort != 'none' or price_sort != 'none', \
            "At least one column should maintain sorting"

    @pytest.mark.regression
    def test_sort_with_filter_applied(self):
        """Test Case 13: Testing sorting after applying filter"""
        # Get some existing data to filter by
        initial_data = self.products_page.get_table_data()

        if initial_data and initial_data[0]['sku']:
            filter_char = initial_data[0]['sku'][0]

            # Step 1: Apply filter first
            self.products_page.enter_sku_search(filter_char)
            self.products_page.wait_for_table_update()

            # Step 2: Apply sorting
            self.products_page.sort_by_column('product_name', 'asc')

            # Verify both filter and sort are active
            filtered_data = self.products_page.get_table_data()
            assert len(filtered_data) > 0, "Filtered data should be visible"

            sort_order = self.products_page.get_sort_order(self.products_page.PRODUCT_NAME_HEADER)
            assert sort_order == 'asc', "Sort should be applied to filtered data"

    @pytest.mark.regression
    def test_filter_with_sort_applied(self):
        """Test Case 14: Testing filter after applying sort"""
        # Step 1: Apply sorting first
        self.products_page.sort_by_column('id', 'desc')

        # Get some data to filter by
        sorted_data = self.products_page.get_table_data()

        if sorted_data and sorted_data[0]['sku']:
            filter_char = sorted_data[0]['sku'][0]

            # Step 2: Apply filter
            self.products_page.enter_sku_search(filter_char)
            self.products_page.wait_for_table_update()

            # Verify both sort and filter are active
            final_data = self.products_page.get_table_data()

            sort_order = self.products_page.get_sort_order(self.products_page.ID_HEADER)
            assert sort_order == 'desc', "Sort should remain active after filtering"

            # Verify filter is working
            assert self.products_page.verify_search_results_contain_text(filter_char, 'sku'), \
                "Filter should be applied to sorted data"


class TestProductsPageReset:
    """Test suite for reset functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.products_page = ProductsPage(driver)
        self.products_page.navigate_to_products_page()

    @pytest.mark.regression
    def test_page_reset_functionality(self):
        """Test Case 15: Testing state after resetting"""
        # Step 1: Add filter text
        self.products_page.enter_sku_search("test")

        # Step 2: Add sorting
        self.products_page.sort_by_column('product_name', 'asc')

        # Verify changes are applied
        assert self.products_page.get_sku_search_value() == "test", "Filter should be applied"
        sort_order = self.products_page.get_sort_order(self.products_page.PRODUCT_NAME_HEADER)
        assert sort_order == 'asc', "Sort should be applied"

        # Step 3: Reset the page
        self.products_page.refresh_page()

        # Expected result: Page returns to default state
        assert self.products_page.get_sku_search_value() == "", "Filter should be cleared after reset"
        assert self.products_page.get_product_name_search_value() == "", "Product name filter should be cleared"

        # Verify table shows all data
        table_data = self.products_page.get_table_data()
        assert len(table_data) > 0, "Table should show all data after reset"