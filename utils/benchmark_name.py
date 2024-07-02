import re

def extract_benchmark(url, app_name):
    # Extrai o caminho da URL
    path = re.search(r'http://[^/]+(/.*)', url)
    if path:
        path = path.group(1).strip('/')
        if not path:
            path = 'home'
    else:
        path = 'home'
    return f"{app_name}-{path}"