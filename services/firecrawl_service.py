from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os

load_dotenv()

app = FirecrawlApp(
    api_key=os.getenv("FIRECRAWL_API_KEY")
)


def map_website(url):

    result = app.map(
        url=url
    )

    return result.links

def scrape_page(url):

    result = app.scrape(
        url,
        formats=["markdown"],
        only_main_content=True
    )

    return result

def scrape_pages(urls):

    scraped_data = []

    for url in urls:

        print(f"Scraping: {url}")

        try:

            result = scrape_page(url)

            scraped_data.append({
                "url": url,
                "content": result.markdown
            })

        except Exception as e:

            print(f"Failed to scrape {url}")
            print(e)

    return scraped_data