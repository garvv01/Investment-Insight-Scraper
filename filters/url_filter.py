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
    "/podcasts"
]


def filter_urls(links):

    filtered_links = []

    for item in links:

        should_skip = False

        for blocked in BLOCKLIST:
            if blocked in item.url:
                should_skip = True
                break

        if not should_skip:
            filtered_links.append({
                "url": item.url,
                "title": item.title,
                "description": item.description
            })

    return filtered_links