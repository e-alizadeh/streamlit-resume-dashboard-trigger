from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

_CV_DASHBOARD_URL = "https://alizadeh-cv.streamlit.app/"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # Navigate to your Streamlit app with increased timeout
            print(f"Navigating to {_CV_DASHBOARD_URL}")
            page.goto(_CV_DASHBOARD_URL, timeout=90000, wait_until="networkidle")
            print(f"Page title: {page.title()}")

            # Wait additional time for Streamlit to fully initialize
            print("Waiting for Streamlit to initialize...")
            page.wait_for_timeout(10000)

            # Wait for the iframe to be attached to the DOM
            print("Waiting for Streamlit iframe to be attached...")
            page.wait_for_selector("iframe[title=\"streamlitApp\"]", timeout=60000, state="attached")
            print("Streamlit iframe found and attached")

            # Now use frame_locator
            iframe = page.frame_locator("iframe[title=\"streamlitApp\"]")

            # Wait for any Streamlit content to load (this proves the app is running)
            print("Waiting for Streamlit content to load...")
            iframe.locator("[data-testid]").first.wait_for(state="attached", timeout=60000)
            print("Streamlit app content loaded successfully")

            # Optional: Try to interact with expander if it exists (non-blocking)
            print("Looking for expander element (optional)...")
            try:
                expander = iframe.get_by_test_id("stExpanderToggleIcon").first
                expander.wait_for(state="visible", timeout=15000)
                expander.scroll_into_view_if_needed(timeout=5000)
                expander.click(timeout=10000)
                print("Expander clicked successfully")
                page.wait_for_timeout(2000)
            except (PlaywrightTimeoutError, Exception) as e:
                # If expander doesn't exist or can't be clicked, that's okay
                # The main goal is just to load the app
                print(f"Could not interact with expander (this is okay): {e}")
                print("App is still considered awake - page was loaded successfully")

            print("Keep-awake task completed successfully")

        except PlaywrightTimeoutError as e:
            print(f"Timeout error: {e}")
            print("Taking screenshot for debugging...")
            page.screenshot(path="debug_timeout.png", full_page=True)
            raise
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Taking screenshot for debugging...")
            page.screenshot(path="debug_error.png", full_page=True)
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    main()