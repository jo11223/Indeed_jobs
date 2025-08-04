# from indeed import get_driver, parse_jobs
# from storage import save_to_json, save_to_mongo
# from config import BASE_URL, SEARCH_PARAMS
# import urllib.parse

# def build_url(start=0):
#     params = SEARCH_PARAMS.copy()
#     params["start"] = start
#     return f"{BASE_URL}?{urllib.parse.urlencode(params)}"

# def main(pages=3):
#     driver = get_driver()
#     all_jobs = []
#     for i in range(pages):
#         url = build_url(start=i * 10)
#         driver.get(url)
#         # optional: explicit waits here for element presence
#         time.sleep(random.uniform(2, 4))  # extra buffer
#         html = driver.page_source
#         jobs = parse_jobs(html)
#         if not jobs:
#             break
#         all_jobs.extend(jobs)
#     driver.quit()
#     save_to_json(all_jobs)
#     save_to_mongo(all_jobs)
#     print(f"Scraped {len(all_jobs)} jobs.")

# if __name__ == "__main__":
#     main()

import time
import random
from scraper.indeed import get_driver, scrape_one_page
from scraper.storage import save_to_json, save_to_mongo


def main(pages=1):
    driver = get_driver()
    all_jobs = []
    try:
        for i in range(pages):
            start = i * 10
            jobs = scrape_one_page(driver, start=start)
            if not jobs:
                print(f"No jobs found on page {i}, stopping.")
                break
            all_jobs.extend(jobs)
            # polite pause before next page
            time.sleep(random.uniform(2, 4))
    finally:
        driver.quit()

    print(f"Scraped {len(all_jobs)} jobs.")
    save_to_json(all_jobs)
    save_to_mongo(all_jobs)


if __name__ == '__main__':
    main(pages=2)  # adjust number of pages