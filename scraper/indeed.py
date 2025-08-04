import time
import random
import urllib.parse
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from config import BASE_URL, SEARCH_PARAMS, DELAY_RANGE
from scraper.user_agents import random_user_agent
import pickle
import os

COOKIE_FILE = "indeed_cookies.pkl"

def save_cookies(driver):
    cookies = driver.get_cookies()
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(cookies, f)
    print(f"[info] Saved {len(cookies)} cookies to {COOKIE_FILE}")

def load_cookies(driver):
    if not os.path.exists(COOKIE_FILE):
        return False
    driver.get("https://www.indeed.com")
    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass
    print(f"[info] Loaded {len(cookies)} cookies from {COOKIE_FILE}")
    return True

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={random_user_agent()}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.headless = False  # Better chance to avoid detection if visible

    # Optional proxy (replace with your own or use a proxy rotation tool)
    # options.add_argument("--proxy-server=http://your.proxy.ip:port")

    driver = uc.Chrome(options=options)
    return driver

def build_url(start=0):
    params = SEARCH_PARAMS.copy()
    params["start"] = start
    return f"{BASE_URL}?{urllib.parse.urlencode(params)}"

def parse_jobs(html):
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.select("article, div.job_seen_beacon"):
        title_elem = card.select_one("h2 a") or card.select_one("h2 a span")
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)
        href = title_elem.get("href") or (title_elem.find_parent("a") and title_elem.find_parent("a").get("href"))
        url = urllib.parse.urljoin("https://www.indeed.com", href) if href else None

        company, location = None, None
        for sel in ["span.companyName", "span.company > a", "span.company", "div.companyName"]:
            el = card.select_one(sel)
            if el:
                company = el.get_text(strip=True)
                break
        for sel in ["div.companyLocation", "div.location", "span.companyLocation"]:
            el = card.select_one(sel)
            if el:
                location = el.get_text(strip=True)
                break

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "url": url,
        })
    return jobs

def scrape_one_page(driver, start=0, max_attempts=2):
    url = build_url(start)
    load_cookies(driver)

    for attempt in range(1, max_attempts + 1):
        driver.get(url)
        time.sleep(8)

        html_lower = driver.page_source.lower()
        if any(p in html_lower for p in ["create an account", "sign in", "continue with google"]):
            print("[info] Manual login required.")
            input("Please log in and press Enter to continue...")
            save_cookies(driver)
            time.sleep(2)

        # Scroll like a human
        for h in [0.3, 0.6, 1.0]:
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {h});")
            time.sleep(random.uniform(1, 2))

        html = driver.page_source
        if "verify you’re human" in html.lower():
            print("[info] CAPTCHA triggered. Solve it manually.")
            input("After solving, press Enter to continue...")
            time.sleep(10)
            html = driver.page_source

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
            )
        except:
            print(f"[warn] Timeout waiting for job cards on attempt {attempt}")

        time.sleep(random.uniform(*DELAY_RANGE))
        jobs = parse_jobs(html)
        if jobs:
            return jobs

        print(f"[retry] Attempt {attempt} failed, retrying...")
        time.sleep(1 + attempt * 1.5)

    with open(f"debug_page_{start}.html", "w", encoding="utf-8") as f:
        f.write(html)
    return []
