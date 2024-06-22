from playwright.sync_api import sync_playwright
import os
_CV_DASHBOARD_URL = "https://alizadeh-cv.streamlit.app/"

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Start recording
    page.video_start_recording(path="recording.webm")

    page.goto(_CV_DASHBOARD_URL)
    page.frame_locator("iframe[title=\"streamlitApp\"]").get_by_test_id("stExpanderToggleIcon").click()


    # Stop recording
    page.video_stop_recording()

    # Close the browser
    browser.close()

with sync_playwright() as playwright:
    run(playwright)

print(f"Recording saved to {os.path.abspath('recording.webm')}")