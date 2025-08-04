# # # import time
# # # import random
# # # import urllib.parse
# # # from selenium import webdriver
# # # from selenium.webdriver.chrome.options import Options
# # # from selenium.webdriver.common.by import By
# # # from bs4 import BeautifulSoup
# # # from config import BASE_URL, SEARCH_PARAMS, DELAY_RANGE
# # # from scraper.user_agents import random_user_agent
# # # from selenium.webdriver.chrome.service import Service


# # # def get_driver():
# # #     options = Options()
# # #     options.add_argument(f"user-agent={random_user_agent()}")
# # #     # options.add_argument("--headless=new")  # uncomment if you want headless
# # #     options.add_argument("--disable-blink-features=AutomationControlled")

# # #     chromedriver_path = r"C:\chromedriver-win64\chromedriver.exe"  # your path
# # #     service = Service(executable_path=chromedriver_path)
# # #     driver = webdriver.Chrome(service=service, options=options)
# # #     return driver

# # # def build_url(start=0):
# # #     params = SEARCH_PARAMS.copy()
# # #     params["start"] = start
# # #     return f"{BASE_URL}?{urllib.parse.urlencode(params)}"


# # # def parse_jobs(html):
# # #     soup = BeautifulSoup(html, "html.parser")
# # #     jobs = []
# # #     for card in soup.select("div.job_seen_beacon, div.slider_container, div.jobsearch-SerpJobCard"):  # flexible fallback
# # #         title_elem = card.select_one("h2 a")
# # #         company_elem = card.select_one("span.companyName") or card.select_one("span.company")
# # #         location_elem = card.select_one("div.companyLocation") or card.select_one("div.location")
# # #         if not title_elem:
# # #             continue
# # #         title = title_elem.get_text(strip=True)
# # #         href = title_elem.get('href')
# # #         url = urllib.parse.urljoin("https://www.indeed.com", href) if href else None
# # #         company = company_elem.get_text(strip=True) if company_elem else None
# # #         location = location_elem.get_text(strip=True) if location_elem else None
# # #         jobs.append({
# # #             "title": title,
# # #             "company": company,
# # #             "location": location,
# # #             "url": url,
# # #         })
# # #     return jobs


# # # def scrape_one_page(driver, start=0):
# # #     url = build_url(start)
# # #     driver.get(url)
# # #     # minimal wait - can improve with WebDriverWait for specific selector
# # #     time.sleep(random.uniform(*DELAY_RANGE))
# # #     html = driver.page_source
# # #     return parse_jobs(html)


# # # scraper/indeed.py

# # import time
# # import random
# # import urllib.parse
# # from selenium import webdriver
# # from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from bs4 import BeautifulSoup
# # from config import BASE_URL, SEARCH_PARAMS, DELAY_RANGE
# # from scraper.user_agents import random_user_agent
# # import pickle
# # import os


# # # adjust to your actual chromedriver location
# # CHROMEDRIVER_PATH = r"C:\chromedriver-win64\chromedriver.exe"

# # COOKIE_FILE = "indeed_cookies.pkl"

# # def save_cookies(driver):
# #     cookies = driver.get_cookies()
# #     with open(COOKIE_FILE, "wb") as f:
# #         pickle.dump(cookies, f)
# #     print(f"[info] Saved {len(cookies)} cookies to {COOKIE_FILE}")

# # def load_cookies(driver):
# #     if not os.path.exists(COOKIE_FILE):
# #         return False
# #     driver.get("https://www.indeed.com")  # base domain to set cookies on
# #     with open(COOKIE_FILE, "rb") as f:
# #         cookies = pickle.load(f)
# #     for cookie in cookies:
# #         # avoid issues with expiry being a float or having sameSite misalignment
# #         try:
# #             driver.add_cookie(cookie)
# #         except Exception:
# #             pass
# #     print(f"[info] Loaded {len(cookies)} cookies from {COOKIE_FILE}")
# #     return True




# # def get_driver():
# #     options = Options()
# #     options.add_argument(f"user-agent={random_user_agent()}")
# #     # options.add_argument("--headless=new")  # leave commented for manual verification during development
# #     options.add_argument("--disable-blink-features=AutomationControlled")
# #     # optional: use a real profile to look more human (be careful not to have profile in use elsewhere)
# #     # options.add_argument(r"--user-data-dir=C:\Users\YourUser\AppData\Local\Google\Chrome\User Data")
# #     # options.add_argument("--profile-directory=Default")

# #     service = Service(executable_path=CHROMEDRIVER_PATH)
# #     driver = webdriver.Chrome(service=service, options=options)
# #     return driver

# # def build_url(start=0):
# #     params = SEARCH_PARAMS.copy()
# #     params["start"] = start
# #     return f"{BASE_URL}?{urllib.parse.urlencode(params)}"

# # # def parse_jobs(html):
# # #     soup = BeautifulSoup(html, "html.parser")
# # #     jobs = []
# # #     # flexible selectors: Indeed changes often
# # #     for card in soup.select("article, div.job_seen_beacon"):
# # #         title_elem = card.select_one("h2 a") or card.select_one("h2 a span")
# # #         company_elem = card.select_one("span.companyName") or card.select_one("span.company")
# # #         location_elem = card.select_one("div.companyLocation") or card.select_one("div.location")
# # #         if not title_elem:
# # #             continue
# # #         title = title_elem.get_text(strip=True)
# # #         href = title_elem.get("href") or (title_elem.find_parent("a") and title_elem.find_parent("a").get("href"))
# # #         url = urllib.parse.urljoin("https://www.indeed.com", href) if href else None
# # #         company = company_elem.get_text(strip=True) if company_elem else None
# # #         location = location_elem.get_text(strip=True) if location_elem else None
# # #         jobs.append({
# # #             "title": title,
# # #             "company": company,
# # #             "location": location,
# # #             "url": url,
# # #         })
# # #     return jobs


# # def parse_jobs(html):
# #     soup = BeautifulSoup(html, "html.parser")
# #     jobs = []

# #     for card in soup.select("article, div.job_seen_beacon"):
# #         # Title / URL
# #         title_elem = card.select_one("h2 a") or card.select_one("h2 a span")
# #         if not title_elem:
# #             continue
# #         title = title_elem.get_text(strip=True)
# #         href = title_elem.get("href") or (title_elem.find_parent("a") and title_elem.find_parent("a").get("href"))
# #         url = urllib.parse.urljoin("https://www.indeed.com", href) if href else None

# #         # Company: try multiple patterns
# #         company = None
# #         comp_sel_candidates = [
# #             "span.companyName",    # current common
# #             "span.company > a",    # fallback if wrapped
# #             "span.company",        # older
# #             "div.companyName",     # sometimes different tag
# #         ]
# #         for sel in comp_sel_candidates:
# #             el = card.select_one(sel)
# #             if el and el.get_text(strip=True):
# #                 company = el.get_text(strip=True)
# #                 break

# #         # Location: try multiple patterns
# #         location = None
# #         loc_sel_candidates = [
# #             "div.companyLocation",
# #             "div.location",
# #             "span.companyLocation",  # edge
# #         ]
# #         for sel in loc_sel_candidates:
# #             el = card.select_one(sel)
# #             if el and el.get_text(strip=True):
# #                 location = el.get_text(strip=True)
# #                 break

# #         # If company or location still missing, optionally log snippet for debugging
# #         if company is None or location is None:
# #             snippet = str(card)[:500]
# #             print(f"[debug] Partial missing info for job '{title}': company={company}, location={location}")
# #             print(f"[debug] Card snippet: {snippet}...")

# #         jobs.append({
# #             "title": title,
# #             "company": company,
# #             "location": location,
# #             "url": url,
# #         })
# #     return jobs


# # # def scrape_one_page(driver, start=0):
# # #     url = build_url(start)
# # #     driver.get(url)

# # #     # initial small pause for dynamic content
# # #     time.sleep(20)

# # #     # detect common human verification/challenge heuristics in page source
# # #     html = driver.page_source
# # #     if "verify you’re human" in html.lower() or "please verify" in html.lower() or "are you a human" in html.lower():
# # #         print("[info] Human verification detected. Please solve it in the browser window, then press Enter to continue...")
# # #         input()  # wait for user to manually intervene
# # #         time.sleep(2)  # let page settle after solving
# # #         html = driver.page_source

# # #     # wait for job card container to appear (timeout 10s)
# # #     try:
# # #         WebDriverWait(driver, 10).until(
# # #             EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
# # #         )
# # #     except Exception:
# # #         print(f"[warning] timed out waiting for job cards on start={start}")

# # #     # polite random delay
# # #     time.sleep(random.uniform(*DELAY_RANGE))

# # #     html = driver.page_source
# # #     jobs = parse_jobs(html)

# # #     if not jobs:
# # #         snippet = html[:2000]
# # #         with open(f"debug_page_{start}.html", "w", encoding="utf-8") as f:
# # #             f.write(html)
# # #         print(f"[debug] No jobs parsed on page start={start}. Saved full HTML to debug_page_{start}.html")
# # #         print(f"[debug] First 1000 chars of page:\n{snippet[:1000]}")
# # #     return jobs
# # # def scrape_one_page(driver, start=0, max_attempts=3):
# # #     url = build_url(start)
# # #     attempt = 0
# # #     while attempt < max_attempts:
# # #         attempt += 1
# # #         driver.get(url)
# # #         time.sleep(10)  # initial settle

# # #         # simple human-like scroll to trigger lazy loads
# # #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
# # #         time.sleep(random.uniform(1, 2))
# # #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
# # #         time.sleep(random.uniform(1, 2))
# # #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# # #         time.sleep(1)

# # #         html = driver.page_source
# # #         # detect challenge
# # #         if any(phrase in html.lower() for phrase in ["verify you’re human", "please verify", "are you a human", "complete the captcha"]):
# # #             print(f"[info] Human verification detected on attempt {attempt}. Solve it manually, then press Enter to continue...")
# # #             input()
# # #             time.sleep(2)
# # #             html = driver.page_source  # refresh after manual solve

# # #         # wait for job cards
# # #         try:
# # #             WebDriverWait(driver, 10).until(
# # #                 EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
# # #             )
# # #         except Exception:
# # #             print(f"[warning] timed out waiting for job cards on start={start}, attempt {attempt}")

# # #         # extra random pause to blend in
# # #         time.sleep(random.uniform(*DELAY_RANGE))

# # #         html = driver.page_source
# # #         jobs = parse_jobs(html)
# # #         if jobs:
# # #             return jobs  # success
# # #         else:
# # #             print(f"[debug] No jobs parsed on attempt {attempt} for start={start}. Retrying...")
# # #             # small backoff before retry
# # #             time.sleep(1 + attempt * 1.5)

# # #     # final fallback after exhausting attempts
# # #     # dump for diagnostics
# # #     snippet = html[:2000]
# # #     with open(f"debug_page_{start}.html", "w", encoding="utf-8") as f:
# # #         f.write(html)
# # #     print(f"[debug] Failed to parse jobs after {max_attempts} attempts. Saved HTML to debug_page_{start}.html")
# # #     print(f"[debug] First 1000 chars:\n{snippet[:1000]}")
# # #     return []
# # def scrape_one_page(driver, start=0, max_attempts=2):
# #     url = build_url(start)

# #     # On first call, try to load saved cookies so we’re authenticated if possible
# #     load_cookies(driver)

# #     attempt = 0
# #     while attempt < max_attempts:
# #         attempt += 1
# #         driver.get(url)
# #         time.sleep(10)  # initial settle

# #         # If we detect the forced login/signup interstitial, give user a chance to authenticate
# #         page_html_lower = driver.page_source.lower()
# #         if ("create an account or sign in" in page_html_lower
# #                 or "continue with google" in page_html_lower
# #                 or "sign in to see more" in page_html_lower):
# #             print("[info] Login/signup gate detected. Please manually log in in the browser window.")
# #             input("After completing login, press Enter to continue...")
# #             # after manual login, save cookies for next runs
# #             save_cookies(driver)
# #             time.sleep(2)  # allow session to settle

# #         # Do human-like scrolling to encourage full load
# #         try:
# #             driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
# #             time.sleep(random.uniform(1, 1.5))
# #             driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
# #             time.sleep(random.uniform(1, 1.5))
# #             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# #         except Exception:
# #             pass

# #         # Detect human-verification challenge (again)
# #         html = driver.page_source
# #         if any(phrase in html.lower() for phrase in ["verify you’re human", "please verify", "are you a human"]):
# #             print(f"[info] Human verification detected on attempt {attempt}. Solve it manually, then press Enter.")
# #             input()
# #             time.sleep(10)
# #             html = driver.page_source  # refresh after solve

# #         # Wait for job cards to appear
# #         try:
# #             WebDriverWait(driver, 10).until(
# #                 EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
# #             )
# #         except Exception:
# #             print(f"[warning] timed out waiting for job cards on start={start}, attempt {attempt}")

# #         time.sleep(random.uniform(*DELAY_RANGE))
# #         html = driver.page_source
# #         jobs = parse_jobs(html)
# #         if jobs:
# #             return jobs

# #         print(f"[debug] No jobs parsed on attempt {attempt} for start={start}. Retrying...")
# #         time.sleep(1 + attempt * 1.0)

# #     # giving up after attempts
# #     snippet = html[:2000]
# #     with open(f"debug_page_{start}.html", "w", encoding="utf-8") as f:
# #         f.write(html)
# #     print(f"[debug] Failed after {max_attempts} attempts. HTML saved to debug_page_{start}.html")
# #     print(f"[debug] Snippet:\n{snippet[:1000]}")
# #     return []





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

# import time
# import random
# import urllib.parse
# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# from config import BASE_URL, SEARCH_PARAMS, DELAY_RANGE
# from scraper.user_agents import random_user_agent

# def get_driver():
#     options = uc.ChromeOptions()
#     options.add_argument(f"user-agent={random_user_agent()}")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.headless = False  # More human-like, avoid detection

#     driver = uc.Chrome(options=options)
#     return driver

# def build_url(start=0):
#     params = SEARCH_PARAMS.copy()
#     params["start"] = start
#     return f"{BASE_URL}?{urllib.parse.urlencode(params)}"

# def parse_jobs(html):
#     soup = BeautifulSoup(html, "html.parser")
#     jobs = []

#     for card in soup.select("article, div.job_seen_beacon"):
#         title_elem = card.select_one("h2 a") or card.select_one("h2 a span")
#         if not title_elem:
#             continue
#         title = title_elem.get_text(strip=True)
#         href = title_elem.get("href") or (title_elem.find_parent("a") and title_elem.find_parent("a").get("href"))
#         url = urllib.parse.urljoin("https://www.indeed.com", href) if href else None

#         company, location = None, None
#         for sel in ["span.companyName", "span.company > a", "span.company", "div.companyName"]:
#             el = card.select_one(sel)
#             if el:
#                 company = el.get_text(strip=True)
#                 break
#         for sel in ["div.companyLocation", "div.location", "span.companyLocation"]:
#             el = card.select_one(sel)
#             if el:
#                 location = el.get_text(strip=True)
#                 break

#         jobs.append({
#             "title": title,
#             "company": company,
#             "location": location,
#             "url": url,
#         })
#     return jobs

# def scrape_one_page(driver, start=0, max_attempts=2):
#     url = build_url(start)

#     for attempt in range(1, max_attempts + 1):
#         driver.get(url)
#         time.sleep(8)

#         # Scroll like a human
#         for h in [0.3, 0.6, 1.0]:
#             driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {h});")
#             time.sleep(random.uniform(1, 2))

#         html = driver.page_source

#         # Check for CAPTCHA/human verification
#         if "verify you’re human" in html.lower() or "please verify" in html.lower():
#             print("[info] CAPTCHA detected. Solve it manually.")
#             input("After solving, press Enter to continue...")
#             time.sleep(10)
#             html = driver.page_source

#         # Wait for job cards
#         try:
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
#             )
#         except:
#             print(f"[warn] Timeout waiting for job cards on attempt {attempt}")

#         time.sleep(random.uniform(*DELAY_RANGE))
#         jobs = parse_jobs(html)
#         if jobs:
#             return jobs

#         print(f"[retry] Attempt {attempt} failed, retrying...")
#         time.sleep(1 + attempt * 1.5)

#     with open(f"debug_page_{start}.html", "w", encoding="utf-8") as f:
#         f.write(html)
#     return []
