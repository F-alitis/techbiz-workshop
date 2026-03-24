NBG_URLS = [
    "https://www.nbg.gr/en/retail",
    "https://www.nbg.gr/en/retail/loans",
    "https://www.nbg.gr/en/retail/cards",
    "https://www.nbg.gr/en/retail/accounts",
    "https://www.nbg.gr/en/business",
    "https://www.nbg.gr/en/about-us",
    "https://www.nbg.gr/en/contact",
]

CRAWL_SETTINGS = {
    "max_depth": 2,
    "rate_limit": 1.0,
    "timeout": 30,
    "allowed_domain": "nbg.gr",
}
