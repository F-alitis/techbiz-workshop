import asyncio
from langchain_core.tools import tool
from src.crawl.crawler import crawl_url


@tool
def scrape_nbg_page(url: str) -> str:
    """Scrape live content from an NBG website page.
    Use for: real-time promotions, current hours, latest announcements.
    Only works for pages under nbg.gr domain.

    Args:
        url: Full URL of the NBG page to scrape

    Returns:
        Page content as clean markdown
    """
    if "nbg.gr" not in url:
        return "Error: Only NBG website URLs (nbg.gr) are allowed."

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                content = pool.submit(asyncio.run, crawl_url(url)).result()
        else:
            content = asyncio.run(crawl_url(url))
        return content if content else "Could not retrieve content from the page."
    except Exception as e:
        return f"Error scraping page: {str(e)}"
