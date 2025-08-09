import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    """Setup Chrome WebDriver with proper configuration."""
    print("Setting up Chrome WebDriver...")
    
    options = webdriver.ChromeOptions()
    
    # Basic Chrome options
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    
    # Remove automation flags
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Remove webdriver property to avoid detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.maximize_window()
        
        print("Chrome WebDriver setup successful!")
        return driver
        
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        raise

def test_chatgpt():
    """Test opening ChatGPT."""
    driver = None
    try:
        driver = setup_driver()
        
        print("Opening ChatGPT...")
        driver.get("https://chat.openai.com/")
        
        # Wait for page to load
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Check if page loaded correctly
        page_title = driver.title
        print(f"Page title: {page_title}")
        
        if "ChatGPT" in page_title or "OpenAI" in page_title:
            print(f"✅ Successfully opened ChatGPT. Page title: {page_title}")
        else:
            print(f"❌ Unexpected page title: {page_title}")
            return False
        
        # Add a small delay to see the page
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        # Take screenshot on error
        if driver:
            try:
                driver.save_screenshot("error_screenshot.png")
                print("Error screenshot saved as error_screenshot.png")
            except:
                print("Could not save error screenshot")
        return False
        
    finally:
        if driver:
            print("Closing Chrome WebDriver...")
            driver.quit()

if __name__ == "__main__":
    print("Starting ChatGPT test...")
    success = test_chatgpt()
    if success:
        print("🎉 Test completed successfully!")
        sys.exit(0)
    else:
        print("💥 Test failed!")
        sys.exit(1)
