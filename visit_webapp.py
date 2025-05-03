import argparse
from datetime import datetime
from playwright.sync_api import sync_playwright

LOG_FILE = "visit_log.txt"
MITM_PROXY = "http://127.0.0.1:8080"

# CLI argümanlarını al
parser = argparse.ArgumentParser(description="Visit a URL through mitmproxy using Playwright")
parser.add_argument("-u", "--url", required=True, help="URL to visit (e.g. https://x.com)")
args = parser.parse_args()

TARGET_URL = args.url

def log_visit(url):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] Visited: {url}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_line)
    print(f"[📝] Logged visit to {LOG_FILE}")

def visit_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True yaparsan tespit edilebilir
        context = browser.new_context(
            proxy={"server": MITM_PROXY},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        page = context.new_page()

        # Bot tespitini azaltmak için sahte mouse ve scroll hareketleri
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        print(f"[🌐] Visiting {url} via proxy...")
        page.goto(url, timeout=30000)

        page.mouse.move(200, 200)
        page.keyboard.press("PageDown")
        page.wait_for_timeout(5000)

        print("[✅] Visit complete.")
        browser.close()
        log_visit(url)

if __name__ == "__main__":
    visit_page(TARGET_URL)