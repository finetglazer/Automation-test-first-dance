from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class DriverFactory:
    @staticmethod
    def get_driver(browser_name="chrome", headless=False):
        """
        Factory method to create WebDriver instance

        Args:
            browser_name (str): Browser name (chrome, firefox, edge)
            headless (bool): Run browser in headless mode

        Returns:
            WebDriver: Configured WebDriver instance
        """
        driver = None

        if browser_name.lower() == "chrome":
            chrome_options = ChromeOptions()
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

        elif browser_name.lower() == "firefox":
            firefox_options = FirefoxOptions()
            if headless:
                firefox_options.add_argument("--headless")

            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)

        driver.maximize_window()
        driver.implicitly_wait(10)
        return driver