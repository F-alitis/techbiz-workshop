import asyncio
import os
import re
from datetime import datetime, timezone

from crawl4ai import AsyncWebCrawler

from src.crawl.nbg_config import NBG_URLS, CRAWL_SETTINGS


def _sanitize_filename(url: str) -> str:
    name = url.replace("https://", "").replace("http://", "")
    name = re.sub(r"[^\w]", "_", name)
    return name


async def crawl_url(url: str, output_dir: str = "data/raw") -> str:
    os.makedirs(output_dir, exist_ok=True)
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        content = result.markdown if result.markdown else ""
        filename = _sanitize_filename(url) + ".md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return content


async def crawl_all(
    urls: list[str] | None = None, output_dir: str = "data/raw"
) -> list[dict]:
    if urls is None:
        urls = NBG_URLS

    os.makedirs(output_dir, exist_ok=True)
    results = []
    rate_limit = CRAWL_SETTINGS.get("rate_limit", 1.0)

    async with AsyncWebCrawler() as crawler:
        for i, url in enumerate(urls):
            try:
                result = await crawler.arun(url=url)
                content = result.markdown if result.markdown else ""
                title = result.metadata.get("title", "") if result.metadata else ""

                filename = _sanitize_filename(url) + ".md"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                results.append(
                    {
                        "url": url,
                        "title": title,
                        "content": content,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )
            except Exception as e:
                print(f"Error crawling {url}: {e}")
                results.append(
                    {
                        "url": url,
                        "title": "",
                        "content": "",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )

            if i < len(urls) - 1:
                await asyncio.sleep(rate_limit)

    return results
