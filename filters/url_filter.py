BLOCKLIST = [
    "/admin",
    "/team",
    "/our-team",
    "/author",
    "/authors",
    "/investor",
    "/privacy",
    "/legal",
    "/terms",
    "/contact",
    "/careers",
    "/jobs",
    "/feed",
    "/login",
    "/signup",
    "/podcast",
    "/podcasts",
    "/about",
    "/media",
    "/press",
    "/newsroom",
    "/events",
    "/webinar",
    "/video",
    "/videos",
    "/newsletter",
    "/cookie",
    "/faq",
    "/support",
    "/job"
]


def filter_urls(links):

    filtered_links = []

    for item in links:

        should_skip = False

        for blocked in BLOCKLIST:
            if blocked in item.url.lower():
                should_skip = True
                break

        if not should_skip:
            filtered_links.append({
                "url": item.url,
                "title": item.title or "",
                "description": item.description or ""
            })

    seen = set()
    unique_links = []

    for item in filtered_links:
         if item["url"] in seen:
             continue
         
         seen.add(item["url"])
         unique_links.append(item)

    return unique_links