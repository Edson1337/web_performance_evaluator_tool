import re


def extract_route(url: str) -> str:
    match = re.search(r'http://[^/]+(/.*)', url)
    if match:
        path = match.group(1).strip('/')
        return path.replace('/', '_') if path else 'home'
    return 'home'