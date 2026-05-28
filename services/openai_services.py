from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def classify_investment_urls(filtered_links):

    response = client.chat.completions.create(
        model="gpt-5.4",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You are filtering URLs from a venture capital website.

Keep URLs that are likely:
- portfolio company pages
- startup spotlight pages
- investment case studies
- funding announcements
- investment thesis articles
- founder stories
- investment insight blogs

Prefer:
- deep content pages
- startup/company-specific pages

Reject URLs that are clearly:
- legal pages
- privacy pages
- admin pages
- login/signup pages
- careers/jobs pages
- podcast pages
- team/about/contact pages

Avoid keeping:
- generic homepage
- generic about/approach pages
unless they contain unique investment insights.

Be generous with potentially useful investment content.

Return JSON in this exact format:

{
  "urls": [
    "https://example.com/page1",
    "https://example.com/page2"
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
  "company_name": "",
  "sector": "",
  "business_summary": "",
  "why_invested": "",
  "market_gap": "",
  "growth_metrics": "",
  "investment_thesis": "",
  "key_challenges": "",
  "category_creation_insight": ""
}

Rules:
- Keep answers concise but informative
- Extract only information clearly present
- Do not hallucinate
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

            insights.append(result)

        except Exception as e:

            print(f"Failed on: {page['url']}")
            print(e)

    return insights