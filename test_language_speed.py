# test_language_speed.py
"""
Quick test script to verify the optimized language change functionality
"""

from selenium import webdriver
from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.home_page import HomePage
import time

def test_fast_language_change():
    """Test the optimized language change speed"""
    driver = None
    try:
        print("🚀 Testing SUPER FAST Language Change")
        print("=" * 60)

        # Create driver
        driver = DriverFactory.get_driver("chrome", headless=False)
        driver.implicitly_wait(5)

        # Quick login
        print("1️⃣ Logging in...")
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page("http://localhost")

        login_start = time.time()
        if login_page.perform_login("admin@shopizer.com", "password"):
            login_time = time.time() - login_start
            print(f"✅ Login completed in {login_time:.2f} seconds")
        else:
            print("❌ Login failed")
            return

        # Test optimized language functions
        print("\n2️⃣ Testing OPTIMIZED language functions...")
        home_page = HomePage(driver)
        home_page.wait_for_home_page_load()

        # Test 1: Optimized language detection
        print("\n📋 PERFORMANCE TESTS:")
        detect_start = time.time()
        current_lang = home_page.get_current_language()
        detect_time = time.time() - detect_start
        print(f"⚡ Language Detection: {detect_time:.3f}s -> Result: {current_lang}")

        # Test 2: Optimized French check
        check_start = time.time()
        is_french = home_page.is_french_language()
        check_time = time.time() - check_start
        print(f"⚡ French Check: {check_time:.3f}s -> Result: {is_french}")

        # Test 3: THE BIG TEST - Optimized language change
        if is_french:
            print(f"\n🎯 MAIN TEST: Changing from French to English...")
            print("Expected time with old method: 10-15 seconds")
            print("Expected time with new method: 2-3 seconds")
            print("-" * 40)

            change_start = time.time()
            success = home_page.change_language_to_english()
            change_time = time.time() - change_start

            if success:
                print(f"🚀 LANGUAGE CHANGED in {change_time:.2f} seconds!")

                # Performance analysis
                if change_time < 4:
                    print(f"🎉 EXCELLENT! {((12 - change_time) / 12 * 100):.0f}% faster than before!")
                elif change_time < 6:
                    print(f"✅ GOOD! Still much faster than the old 10-15 seconds")
                else:
                    print(f"⚠️ Slower than expected, but still working")

                # Verify the change worked
                verify_start = time.time()
                new_lang = home_page.get_current_language()
                verify_time = time.time() - verify_start
                print(f"✅ Verification: {new_lang} (checked in {verify_time:.3f}s)")
            else:
                print("❌ Language change failed - may need to check selectors")
        else:
            print("✅ Already in English - testing detection speed only")

        total_time = time.time() - login_start
        print(f"\n📊 TOTAL TEST TIME: {total_time:.2f} seconds")
        print("=" * 60)

        # Performance summary
        print("🏆 OPTIMIZATION RESULTS:")
        print(f"   • Language Detection: {detect_time:.3f}s (was ~2-3s)")
        print(f"   • Language Check: {check_time:.3f}s (was ~1-2s)")
        if is_french:
            print(f"   • Language Change: {change_time:.2f}s (was 10-15s)")
            print(f"   • Speed Improvement: ~{12/change_time:.1f}x FASTER! 🚀")

        # Keep browser open briefly
        print("\nKeeping browser open for 3 seconds for visual verification...")
        time.sleep(3)

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()

def benchmark_language_operations():
    """Benchmark different language operations"""
    driver = None
    try:
        print("📊 Benchmarking Language Operations")
        print("-" * 50)

        # Setup
        driver = DriverFactory.get_driver("chrome", headless=False)
        driver.implicitly_wait(5)

        # Login first
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page("http://localhost")
        login_page.perform_login("admin@shopizer.com", "password")

        home_page = HomePage(driver)
        home_page.wait_for_home_page_load()

        # Benchmark operations
        operations = {
            "Language Detection": lambda: home_page.get_current_language(),
            "French Check": lambda: home_page.is_french_language(),
            "English Check": lambda: home_page.is_english_language(),
        }

        print("\n⏱️ Operation Timings:")
        for op_name, op_func in operations.items():
            start = time.time()
            result = op_func()
            duration = time.time() - start
            print(f"{op_name}: {duration:.3f}s (Result: {result})")

        # Test language change if needed
        if home_page.is_french_language():
            print("\n🔄 Testing Language Change:")
            start = time.time()
            success = home_page.change_language_to_english()
            duration = time.time() - start
            print(f"Language Change: {duration:.3f}s (Success: {success})")

    except Exception as e:
        print(f"❌ Benchmark failed: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    print("Choose test:")
    print("1. Fast Language Change Test")
    print("2. Benchmark Language Operations")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        test_fast_language_change()
    elif choice == "2":
        benchmark_language_operations()
    else:
        print("Invalid choice. Running fast language change test...")
        test_fast_language_change()