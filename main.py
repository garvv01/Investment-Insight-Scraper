from services.firecrawl_service import map_website,scrape_pages
from services.openai_services import find_content_hubs, extract_all_insights, find_article_urls, filter_top_articles
from filters.url_filter import filter_urls
import json
import os

links = map_website(
    "https://www.titancapital.vc"
)

filtered_links = filter_urls(links)

content_hub_links = find_content_hubs(filtered_links)

content_hub_links = json.loads(content_hub_links)

content_hub_links = content_hub_links["urls"]

hub_scraped_content = scrape_pages(
    content_hub_links
)

all_article_urls = []

for page in hub_scraped_content:

    article_urls = find_article_urls(
        page["content"]
    )

    article_urls = json.loads(article_urls)

    all_article_urls.extend(
        article_urls["urls"]
    )

all_article_urls = list(
    set(all_article_urls)
)

filtered_article_urls = []

BLOCKLIST = [
    "/category/",
    "/tag/",
    "/author/",
    "/page/",
    "/media/",
    "/blogs",
    "/homeblog",
    "/news-and-insights"
]

for url in all_article_urls:

    if any(blocked in url for blocked in BLOCKLIST):
        continue

    filtered_article_urls.append(url)

top_articles = filter_top_articles(
    filtered_article_urls
)

top_articles = json.loads(
    top_articles
)

top_articles = top_articles["urls"]

scraped_articles = scrape_pages(
    top_articles
)

all_insights = extract_all_insights(
    scraped_articles
)

os.makedirs("output", exist_ok=True)

with open("output/insights.json", "w") as file:    
    json.dump(all_insights, file, indent=4)