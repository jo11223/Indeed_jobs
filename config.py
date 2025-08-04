BASE_URL = "https://www.indeed.com/jobs"
SEARCH_PARAMS = {
    "q": "software engineer",
    "l": "Remote",
}
RESULTS_PER_PAGE = 10  # Indeed uses start= increments
DELAY_RANGE = (2, 5)  # seconds
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "job_listings"
COLLECTION = "indeed"
