# pages/__init__.py
"""
Page Object Model package for Selenium automation testing
"""

# Import all page classes for easy access
from .base_page import BasePage
from .login_page import LoginPage
from .home_page import HomePage
from .products_page import ProductsPage
from .product_groups_page import ProductGroupsPage

__all__ = [
    'BasePage',
    'LoginPage',
    'HomePage',
    'ProductsPage',
    'ProductGroupsPage'
]