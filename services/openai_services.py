from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def find_content_hubs(filtered_links):

    response = client.chat.completions.create(
        model="gpt-5.4",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You are analyzing URLs from a venture capital website.

Your task:
Identify URLs that are likely content hubs containing:
- blogs
- articles
- insights
- news
- perspectives
- founder stories
- spotlight pages
- investment writeups
- newsroom content

Return ONLY the TOP 10 most relevant URLs.

Prioritize:
- article index pages
- insights sections
- writing sections
- blog archives
- newsrooms
- spotlight/article collections

Do NOT return:
- homepage
- company profile pages
- portfolio company pages
- team pages
- contact pages
- legal/privacy pages
- login/admin pages

Return JSON in this exact format:

{
  "urls": [
    "https://example.com/blog",
    "https://example.com/insights"
  ]
}
"""
            },
            {
                "role": "user",
                "content": json.dumps(filtered_links)
            }
        ]
    )

    return response.choices[0].message.content

def find_article_urls(scraped_content):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You are analyzing scraped VC website content.

Your task:
Extract the TOP 10 article/blog/news/spotlight URLs
most likely to contain:

- startup investment information
- funding announcements
- investment rationale
- founder stories
- investment theses
- portfolio insights

Prioritize:
- individual article URLs
- blog post URLs
- insight article URLs
- spotlight pages
- funding news pages

Do NOT return:
- category pages
- archive pages
- homepage URLs
- pagination URLs
- tag pages
- author pages

Return JSON in this exact format:

{
  "urls": [
    "https://example.com/article-1",
    "https://example.com/article-2"
  ]
}
"""
            },
            {
                "role": "user",
                "content": scraped_content
            }
        ]
    )

    return response.choices[0].message.content

def filter_top_articles(article_urls):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You are selecting the BEST investment-related articles from a VC website.

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

Avoid:
- category pages
- media archives
- generic hubs
- pagination pages
- videos
- podcasts
- author pages

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
                "content": json.dumps(article_urls)
            }
        ]
    )

    return response.choices[0].message.content

def extract_investment_insight(content):

    response = client.chat.completions.create(
        model="gpt-5.4",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content":"""
You are extracting structured investment insights from VC website content.

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
- Do not hallucinate missing funding stages or amounts
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

            if not result["company_invested_in"]:
                continue

            insights.append(result)

        except Exception as e:

            print(f"Failed on: {page['url']}")
            print(e)

    return insights