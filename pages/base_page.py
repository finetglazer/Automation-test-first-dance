from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import os

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator, timeout=10):
        """Find element with explicit wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            print(f"Element not found with locator: {locator}")
            return None

    def find_elements(self, locator, timeout=10):
        """Find multiple elements with explicit wait"""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            print(f"Elements not found with locator: {locator}")
            return []

    def click_element(self, locator, timeout=10):
        """Click element with explicit wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return True
        except TimeoutException:
            print(f"Element not clickable: {locator}")
            return False

    def enter_text(self, locator, text, timeout=10):
        """Enter text in input field"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            element.clear()
            element.send_keys(text)
            return True
        except TimeoutException:
            print(f"Cannot enter text in element: {locator}")
            return False

    def get_text(self, locator, timeout=10):
        """Get text from element"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.text
        except TimeoutException:
            print(f"Cannot get text from element: {locator}")
            return ""

    def is_element_visible(self, locator, timeout=10):
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def take_screenshot(self, filename):
        """Take screenshot and save it"""
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"{screenshot_dir}/{filename}_{timestamp}.png"
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path

    def scroll_to_element(self, locator):
        """Scroll to element"""
        element = self.find_element(locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url

    def get_page_title(self):
        """Get current page title"""
        return self.driver.title