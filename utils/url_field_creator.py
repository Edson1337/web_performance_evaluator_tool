def create_url(local_host: str, route: str):
    if route == 'home':
        return local_host
    if route != "":
        passed_url = f"{local_host}/{route}"
        return passed_url

    passed_url = f"{local_host}"
    print(f"URL: {passed_url}")
    return passed_url