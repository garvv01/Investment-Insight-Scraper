from services.firecrawl_service import map_website,scrape_pages
from services.openai_services import classify_investment_urls, extract_all_insights
from filters.url_filter import filter_urls
import json
import os

links = map_website(
    "https://www.wehventures.com"
)

filtered_links = filter_urls(links)

investment_links = classify_investment_urls(filtered_links)

investment_links = json.loads(investment_links)

investment_links = investment_links["urls"]

investment_links.sort(
    key=lambda url: (
        "spotlight-page" not in url,
        "portfolio" in url
    )
)

scraped_content = scrape_pages(investment_links)

all_insights = extract_all_insights(
    scraped_content
)

parsed_insights = []

for insight in all_insights:
    parsed_insights.append(
        json.loads(insight)
    )

os.makedirs("output", exist_ok=True)

with open(
    "output/insights.json",
    "w",
    encoding="utf-8"
) as file:
    
    json.dump(
        parsed_insights,
        file,
        indent=4,
        ensure_ascii=False
    )

print("Insights saved successfully")