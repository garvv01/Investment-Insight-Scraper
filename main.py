from services.firecrawl_service import map_website, scrape_pages
from services.openai_services import filter_top_articles, decide_route, extract_all_insights
from filters.url_filter import filter_urls
import json
import os

links = map_website(
    "https://www.titancapital.vc"
)

cleaned_links = filter_urls(links)

route_decision = decide_route(cleaned_links)

route_decision = json.loads(route_decision)

print("\nROUTE DECISION:\n")
print(route_decision)

if route_decision["route"]=="route_1":

    print("\nUSING ROUTE 1\n")

    top_articles = filter_top_articles(cleaned_links)

    top_articles = json.loads(top_articles)

    top_articles = top_articles["urls"]

    print("\nTop investment-related URLs found:\n")

    for url in top_articles:
        print(url)

    scraped_articles = scrape_pages(
        top_articles
    )

    all_insights = extract_all_insights(
        scraped_articles
    )

    os.makedirs("output", exist_ok=True)

    with open("output/insights.json", "w") as file:
        json.dump(all_insights, file, indent=4)

    print("\nSaved insights to output/insights.json")

else:

    print("\nUSING ROUTE 2\n")