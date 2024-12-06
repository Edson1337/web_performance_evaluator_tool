def reset_setup_json(parsed_json):
    parsed_json['performance_evaluation']['project_name'] = ""
    parsed_json['performance_evaluation']['app_name'] = ""
    parsed_json['performance_evaluation']['url'] = ""
    parsed_json['performance_evaluation']['performance_evaluation_id'] = ""
    parsed_json['performance_evaluation']['scenarios'] = []
    parsed_json['performance_evaluation']['metrics'] = [
        "firstContentfulPaint",
        "largestContentfulPaint",
        "fullyLoaded",
        "ttfb",
        "totalBlockingTime"
    ]