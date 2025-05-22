import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class TestSampleWebsite:
    """Sample test class for black box testing"""

    def test_page_title(self, driver_with_base_url):
        """Test if page title is loaded correctly"""
        page = BasePage(driver_with_base_url)
        title = page.get_page_title()
        assert title is not None, "Page title should not be None"
        assert len(title) > 0, "Page title should not be empty"

    def test_page_loads_successfully(self, driver_with_base_url):
        """Test if page loads without errors"""
        page = BasePage(driver_with_base_url)
        current_url = page.get_current_url()
        assert "example.com" in current_url, "Should be on the correct domain"

    @pytest.mark.smoke
    def test_basic_navigation(self, driver):
        """Test basic navigation functionality"""
        page = BasePage(driver)

        # Navigate to a test site
        driver.get("https://www.google.com")

        # Check if search box is present
        search_box_locator = (By.NAME, "q")
        assert page.is_element_visible(search_box_locator), "Search box should be visible"

        # Enter search text
        search_text = "Selenium WebDriver"
        assert page.enter_text(search_box_locator, search_text), "Should be able to enter text"

        # Take screenshot
        screenshot_path = page.take_screenshot("navigation_test")
        assert screenshot_path, "Screenshot should be taken"

    @pytest.mark.regression
    def test_form_validation(self, driver):
        """Test form validation (example with a demo site)"""
        # You can replace this with your actual application URL
        driver.get("https://demoqa.com/text-box")
        page = BasePage(driver)

        # Test form elements
        full_name_locator = (By.ID, "userName")
        email_locator = (By.ID, "userEmail")
        submit_locator = (By.ID, "submit")

        # Test if elements are visible
        assert page.is_element_visible(full_name_locator), "Full name field should be visible"
        assert page.is_element_visible(email_locator), "Email field should be visible"

        # Fill form
        page.enter_text(full_name_locator, "John Doe")
        page.enter_text(email_locator, "john.doe@example.com")

        # Submit form
        page.scroll_to_element(submit_locator)
        page.click_element(submit_locator)

        # Take screenshot after submission
        page.take_screenshot("form_submission")

    def test_responsive_design(self, driver):
        """Test responsive design by changing window size"""
        page = BasePage(driver)
        driver.get("https://www.google.com")

        # Test different screen sizes
        screen_sizes = [
            (1920, 1080),  # Desktop
            (768, 1024),   # Tablet
            (375, 667)     # Mobile
        ]

        for width, height in screen_sizes:
            driver.set_window_size(width, height)

            # Check if search box is still accessible
            search_box_locator = (By.NAME, "q")
            assert page.is_element_visible(search_box_locator), f"Search box should be visible at {width}x{height}"

            # Take screenshot for each size
            page.take_screenshot(f"responsive_{width}x{height}")

# Example of parametrized test
class TestDataDriven:
    """Example of data-driven testing"""

    @pytest.mark.parametrize("search_term,expected_result", [
        ("Selenium", "selenium"),
        ("Python", "python"),
        ("Testing", "testing")
    ])
    def test_search_functionality(self, driver, search_term, expected_result):
        """Test search with different terms"""
        page = BasePage(driver)
        driver.get("https://www.google.com")

        search_box_locator = (By.NAME, "q")
        page.enter_text(search_box_locator, search_term)

        # Press Enter or click search button
        search_button_locator = (By.NAME, "btnK")
        page.click_element(search_button_locator)

        # Wait for results and verify
        page_title = page.get_page_title().lower()
        assert expected_result in page_title, f"Search results should contain '{expected_result}'"