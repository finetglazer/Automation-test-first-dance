import os

class Config:
    # Browser Configuration
    BROWSER = os.getenv('BROWSER', 'chrome')  # chrome, firefox, edge
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'

    # Test Environment URLs - FIXED BASE URL
    BASE_URL = os.getenv('BASE_URL', 'http://localhost')  # Updated from https://example.com
    STAGING_URL = os.getenv('STAGING_URL', 'http://localhost:8080')  # Added port variant

    # Timeouts
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
    PAGE_LOAD_TIMEOUT = 30

    # Test Data
    VALID_USERNAME = os.getenv('VALID_USERNAME', 'admin@shopizer.com')  # Updated default
    VALID_PASSWORD = os.getenv('VALID_PASSWORD', 'password')  # Updated default

    # Directories
    SCREENSHOTS_DIR = 'screenshots'
    REPORTS_DIR = 'reports'
    TEST_DATA_DIR = 'test_data'

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def get_url(cls, environment='base'):
        """Get URL based on environment"""
        urls = {
            'base': cls.BASE_URL,
            'staging': cls.STAGING_URL
        }
        return urls.get(environment, cls.BASE_URL)