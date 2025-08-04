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