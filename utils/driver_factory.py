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
        Optimized factory method to create WebDriver instance with faster startup

        Args:
            browser_name (str): Browser name (chrome, firefox, edge)
            headless (bool): Run browser in headless mode

        Returns:
            WebDriver: Configured WebDriver instance
        """
        driver = None

        if browser_name.lower() == "chrome":
            chrome_options = ChromeOptions()

            # Basic options
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")

            # PERFORMANCE OPTIMIZATIONS - These significantly reduce startup time
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")  # Faster page loading
            chrome_options.add_argument("--disable-javascript")  # Remove if your app needs JS
            chrome_options.add_argument("--disable-css")  # Remove if you need styling

            # DISABLE ML/AI FEATURES (fixes TensorFlow warnings)
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-features=BlinkGenPropertyTrees")
            chrome_options.add_argument("--disable-machine-learning-model-download")
            chrome_options.add_argument("--disable-component-extensions-with-background-pages")

            # DISABLE UNNECESSARY FEATURES
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-client-side-phishing-detection")
            chrome_options.add_argument("--disable-sync")
            chrome_options.add_argument("--disable-translate")
            chrome_options.add_argument("--disable-ipc-flooding-protection")

            # MEMORY AND CPU OPTIMIZATIONS
            chrome_options.add_argument("--memory-pressure-off")
            chrome_options.add_argument("--max_old_space_size=4096")
            chrome_options.add_argument("--aggressive-cache-discard")

            # NETWORK OPTIMIZATIONS
            chrome_options.add_argument("--aggressive")
            chrome_options.add_argument("--disable-background-networking")

            # LOGGING OPTIMIZATIONS (reduce console spam)
            chrome_options.add_argument("--log-level=3")  # Only fatal errors
            chrome_options.add_argument("--silent")
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # FASTER PREFERENCES
            prefs = {
                "profile.default_content_setting_values": {
                    "notifications": 2,  # Block notifications
                    "media_stream": 2,   # Block media access
                    "geolocation": 2     # Block location access
                },
                "profile.managed_default_content_settings": {
                    "images": 2          # Block images for faster loading
                }
            }
            chrome_options.add_experimental_option("prefs", prefs)

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

        elif browser_name.lower() == "firefox":
            firefox_options = FirefoxOptions()
            if headless:
                firefox_options.add_argument("--headless")

            # Firefox optimizations
            firefox_options.add_argument("--disable-extensions")
            firefox_options.add_argument("--disable-plugins")

            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)

        # OPTIMIZED TIMEOUTS - Shorter for better performance
        driver.maximize_window()
        driver.implicitly_wait(5)  # Reduced from 10 to 5 seconds
        driver.set_page_load_timeout(15)  # Add page load timeout

        return driver