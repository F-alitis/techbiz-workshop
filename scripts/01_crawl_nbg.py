import asyncio
import sys

sys.path.insert(0, ".")
from src.crawl.crawler import crawl_all


async def main():
    print("Crawling NBG website...")
    results = await crawl_all()
    print(f"Crawled {len(results)} pages")
    for r in results:
        print(f"  - {r['url']}: {len(r['content'])} chars")


if __name__ == "__main__":
    asyncio.run(main())
