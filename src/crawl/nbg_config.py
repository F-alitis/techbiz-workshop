from config.settings import settings

NBG_URLS = settings.nbg_crawl_urls

CRAWL_SETTINGS = {
    "max_depth": settings.crawl_max_depth,
    "rate_limit": settings.crawl_rate_limit,
    "timeout": settings.crawl_timeout,
    "allowed_domain": settings.crawl_allowed_domain,
}
