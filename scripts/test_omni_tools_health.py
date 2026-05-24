import asyncio
import sys
from playwright.async_api import async_playwright

async def run_health_check(url="http://localhost:8080"):
    print(f"Starting Omni Tools health check on {url}...")
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # 1. Navigation Check
            await page.goto(url, timeout=5000)
            print("✓ Successfully navigated to Omni Tools home.")

            # 2. Key Module Verification
            # We check for common tool names in the sidebar or main navigation
            modules = ["JSON Formatter", "Image Converter", "PDF Tools", "Hash Generator"]
            for module in modules:
                # Assuming the tool name is present in the text content
                if await page.get_by_text(module, exact=False).is_visible():
                    print(f"✓ Module found: {module}")
                else:
                    print(f"⚠ Warning: Module '{module}' not immediately visible.")

            # 3. Interactive Test (JSON Formatter)
            # Find the JSON tool and verify it loads
            await page.get_by_text("JSON Formatter").first.click()
            await page.wait_for_selector("textarea", timeout=3000)
            print("✓ JSON Formatter interaction successful.")

            await browser.close()
            print("\nHealth check PASSED.")
            return True
        except Exception as e:
            print(f"\nHealth check FAILED: {str(e)}")
            return False

if __name__ == "__main__":
    # Allow URL override via CLI
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    success = asyncio.run(run_health_check(target_url))
    sys.exit(0 if success else 1)
