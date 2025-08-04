# scraper/user_agents.py
from fake_useragent import UserAgent

_ua = UserAgent()

def random_user_agent():
    try:
        return _ua.random
    except Exception:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
