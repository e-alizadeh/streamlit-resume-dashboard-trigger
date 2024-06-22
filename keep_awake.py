from playwright.sync_api import sync_playwright
import time

_CV_DASHBOARD_URL = "https://alizadeh-cv.streamlit.app/"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Navigate to your Streamlit app
        page.goto(_CV_DASHBOARD_URL)
        print(f"Page title: {page.title()}")
        
        # Wait for the app to load (adjust time if needed)
        time.sleep(5)
        
        # Click on the expander
        expander = page.frame_locator("iframe[title=\"streamlitApp\"]").get_by_test_id("stExpanderToggleIcon")
        expander.click()
        
        print("Expander clicked successfully")
        
        # Wait a bit to allow any animations to complete
        time.sleep(2)
        
        browser.close()

if __name__ == "__main__":
    main()