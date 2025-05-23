import pytest
from pages.product_types_page import ProductTypesPage
import time

class TestProductTypesPageBasic:
    """Test suite for basic functionality with authentication"""

    @pytest.fixture(autouse=True)
    def setup(self, product_types_page_ready):
        self.driver = product_types_page_ready
        self.product_types_page = ProductTypesPage(self.driver)
        self.product_types_page.navigate_to_product_types_page()

    @pytest.mark.smoke
    def test_page_title(self):
        """Verify the page title is correct"""
        assert self.product_types_page.is_element_visible(self.product_types_page.PAGE_TITLE), \
            "Product Types page title should be visible"

    @pytest.mark.smoke
    def test_table_displays(self):
        """Verify the table is displayed on the page"""
        assert self.product_types_page.is_element_visible(self.product_types_page.TABLE), \
            "Product Types table should be visible"


class TestProductTypesPageFilters:
    """Test suite for filter functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, product_types_page_ready):
        self.driver = product_types_page_ready
        self.product_types_page = ProductTypesPage(self.driver)
        self.product_types_page.navigate_to_product_types_page()

    @pytest.mark.regression
    def test_special_characters_filter(self):
        """Test Case 1: Submit special characters into Code field"""
        # Test with emoji
        special_chars = ["🥶🥶", "<script>", "+", "*", "@#$%"]

        for char in special_chars:
            self.product_types_page.enter_code_search(char)
            table_data = self.product_types_page.get_table_data()
            assert len(table_data) == 0, f"Table should show no data for special character: {char}"

    @pytest.mark.smoke
    def test_valid_code_filter(self):
        """Test Case 2: Submit valid text for existing Code name"""
        # Get initial data to find existing code
        initial_data = self.product_types_page.get_table_data()

        if initial_data and initial_data[0]['code']:
            existing_code = initial_data[0]['code']
            search_char = existing_code[0]  # Use first character of existing code

            self.product_types_page.enter_code_search(search_char)
            filtered_data = self.product_types_page.get_table_data()

            assert len(filtered_data) > 0, "Table should show matching data"
            assert self.product_types_page.verify_search_results_contain_text(search_char, 'code'), \
                "All results should contain the search character"

    @pytest.mark.regression
    def test_nonexistent_code_filter(self):
        """Test Case 3: Submit text not existing for Code"""
        # Use a random string that likely won't exist
        self.product_types_page.enter_code_search("xyz123nonexistent")

        table_data = self.product_types_page.get_table_data()
        assert len(table_data) == 0, "Table should show no data for non-existent code"

    @pytest.mark.regression
    def test_spaces_in_code_filter(self):
        """Test Case 4: Submit text with space at beginning or end"""
        # Get initial data to find existing code
        initial_data = self.product_types_page.get_table_data()

        if initial_data and initial_data[0]['code']:
            existing_code = initial_data[0]['code']

            # Test with space at beginning
            self.product_types_page.enter_code_search(f" {existing_code}")
            filtered_data1 = self.product_types_page.get_table_data()

            # Test with space at end
            self.product_types_page.enter_code_search(f"{existing_code} ")
            filtered_data2 = self.product_types_page.get_table_data()

            # Check if spaces are trimmed (results should be the same as without spaces)
            self.product_types_page.enter_code_search(existing_code)
            exact_match_data = self.product_types_page.get_table_data()

            assert len(filtered_data1) == len(exact_match_data) or len(filtered_data2) == len(exact_match_data), \
                "Filter should handle spaces at beginning or end"

    @pytest.mark.security
    def test_security_injection_attempts(self):
        """Test Case 5: Test SQL/XSS injection attempts"""
        injection_attempts = [
            "<script>alert('test')</script>",
            "'; DROP TABLE users; --",
            "<h1>test</h1>"
        ]

        for injection in injection_attempts:
            self.product_types_page.enter_code_search(injection)
            table_data = self.product_types_page.get_table_data()
            assert len(table_data) == 0, f"No data should be shown for injection attempt: {injection}"

    @pytest.mark.smoke
    def test_empty_filter(self):
        """Test Case 6: Submit nothing to test default filter"""
        # First get count of all records
        initial_data = self.product_types_page.get_table_data()
        initial_count = len(initial_data)

        # Clear filter field
        self.product_types_page.enter_code_search("")

        # Get new data
        filtered_data = self.product_types_page.get_table_data()
        assert len(filtered_data) == initial_count, "All records should be displayed with empty filter"

    @pytest.mark.regression
    def test_large_value_filter(self):
        """Test Case 7: Submit large value to test field limits"""
        large_text = "A" * 1000  # 1000 character string

        self.product_types_page.enter_code_search(large_text)

        # Check if the input accepted the value
        actual_value = self.product_types_page.get_code_search_value()
        assert len(actual_value) > 0, "Input should accept some part of the large text"

        # Check table results
        table_data = self.product_types_page.get_table_data()
        assert len(table_data) == 0, "No data should match the oversized input"


class TestProductTypesPageSorting:
    """Test suite for sorting functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, product_types_page_ready):
        self.driver = product_types_page_ready
        self.product_types_page = ProductTypesPage(self.driver)
        self.product_types_page.navigate_to_product_types_page()

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