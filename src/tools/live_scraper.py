import httpx
from bs4 import BeautifulSoup
from langchain_core.tools import tool


def _html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


@tool
def scrape_nbg_page(url: str) -> str:
    """Scrape live content from an NBG website page.
    Use for: real-time promotions, current hours, latest announcements.
    Only works for pages under nbg.gr domain.

    Args:
        url: Full URL of the NBG page to scrape

    Returns:
        Page content as clean text
    """
    if "nbg.gr" not in url:
        return "Error: Only NBG website URLs (nbg.gr) are allowed."

    try:
        response = httpx.get(url, timeout=30, follow_redirects=True)
        response.raise_for_status()
        content = _html_to_text(response.text)
        return content[:5000] if content else "Could not retrieve content from the page."
    except Exception as e:
        return f"Error scraping page: {str(e)}"
