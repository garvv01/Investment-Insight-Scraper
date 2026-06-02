from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def filter_top_articles(article_urls):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You are selecting the BEST investment-related URLs from a VC website.

Your task:
Return ONLY the TOP 10 URLs most likely to contain:

- startup investment insights
- funding announcements
- investment rationale
- founder stories
- portfolio deep dives
- sector theses
- investor commentary

Prioritize URLs containing:
- funding
- raises
- investment
- insight
- spotlight
- seed
- series-a
- startup
- portfolio

Prioritize URLs whose:
- title suggests funding/investment activity
- description mentions startups, funding, investors, or rounds

Avoid:
- category pages
- media archives
- generic hubs
- pagination pages
- videos
- podcasts
- author pages
- team/about/contact/legal pages

You will receive:
[
  {
    "url": "",
    "title": "",
    "description": ""
  }
]

Return JSON in this exact format:

{
  "urls": [
    "https://example.com/article1",
    "https://example.com/article2"
  ]
}
"""
            },
            {
                "role": "user",
                "content": str(article_urls)
            }
        ]
    )

    return response.choices[0].message.content

def extract_investment_insight(content):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You are extracting structured investment insights from VC investment articles.

Return JSON in this exact format:

{
  "source_url": "",
  "company_invested_in": "",
  "stage": "",
  "sector": "",
  "amount_invested": "",
  "co_investors": [],
  "investment_date": "",
  "insights": []
}

Rules:
- insights should contain multiple short bullet-style investment insights
- Extract only explicitly available information
- Do not hallucinate missing information
- Use empty string if unavailable
- Use empty array if unavailable
- Return valid JSON only
"""
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )

    return response.choices[0].message.content

def extract_all_insights(scraped_content):

    insights = []

    for page in scraped_content:

        print(f"Extracting insights from: {page['url']}")

        try:

            result = extract_investment_insight(
                page["content"]
            )

            result = json.loads(result)

            result["source_url"] = page["url"]

            if not result["company_invested_in"]:
                continue

            insights.append(result)

        except Exception as e:

            print(f"Failed on: {page['url']}")
            print(e)

    return insights

def decide_route(mapped_links):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You are deciding which scraping route to use for a VC website.

ROUTE 1:
Use when mapped URLs already contain strong investment/article signals like:
- funding
- raises
- seed
- series-a
- investment
- spotlight
- founder stories
- startup news

ROUTE 2:
Use when mapped URLs are mostly:
- homepage pages
- admin pages
- sitemap pages
- generic portfolio pages
- static pages

Return JSON in this exact format:

{
  "route": "route_1",
  "reason": "Mapped URLs already contain strong investment article signals."
}

OR

{
  "route": "route_2",
  "reason": "Mapped URLs do not contain enough direct article/investment URLs."
}
"""
            },
            {
                "role": "user",
                "content": str(mapped_links)
            }
        ]
    )

    return response.choices[0].message.content