from utils.route_name import extract_route


def extract_benchmark(url, app_name):
    path = extract_route(url)
    return f"{app_name}-{path}"