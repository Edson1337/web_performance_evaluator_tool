from functools import reduce


def get_value(object, path):
    value = reduce(lambda obj, key: obj.get(key, None) if obj else None, path.split('.'), object)
    return value if value is not None else "N/A"

def get_metric_value(metric, verify_browsertime_json, verify_pagexray_json):
    google_web_vitals = verify_browsertime_json.get('googleWebVitals')
    cpu_metrics = verify_browsertime_json.get('cpu')

    metric_mappings = {
        'firstContentfulPaint': lambda: get_value(verify_browsertime_json, 'paintTiming.first-contentful-paint.mean'),
        'totalBlockingTime': lambda: "N/A" if google_web_vitals is None else get_value(google_web_vitals, 'totalBlockingTime.mean'),
        'largestContentfulPaint': lambda: get_value(google_web_vitals, 'largestContentfulPaint.mean'),
        'cumulativeLayoutShift': lambda: "N/A" if google_web_vitals is None else get_value(google_web_vitals, 'cumulativeLayoutShift.mean'),
        'pageLoadTime': lambda: get_value(verify_browsertime_json['pageTimings'], 'pageLoadTime.mean'),
        'ttfb': lambda: get_value(verify_browsertime_json['navigationTiming'], 'responseStart.mean') if google_web_vitals is None else get_value(google_web_vitals, 'ttfb.mean'),
        'maxPotentialFid': lambda: "N/A" if cpu_metrics is None else get_value(cpu_metrics['longTasks'], 'maxPotentialFid.mean'),
    }

    return metric_mappings.get(metric, lambda: "Metric not found")()

def handle_requests_and_content_size(metric, verify_pagexray_json, content_types):
    if metric == 'requests':
        return calculate_requests(content_types)
    elif metric == 'contentSize':
        return calculate_content_size(verify_pagexray_json, content_types)

def calculate_requests(content_types):
    results = {'totalRequests': {}}
    total_requests = 0
    for content_type, data in content_types.items():
        requests_mean = get_value(data['requests'], 'mean')
        results['totalRequests'][content_type] = requests_mean if requests_mean != "N/A" else 0
        total_requests += results['totalRequests'][content_type]
    results['totalRequests']['total'] = total_requests
    return results

def calculate_content_size(verify_pagexray_json, content_types):
    results = {'totalContentSize': {'total': get_value(verify_pagexray_json['contentSize'], 'mean')}}
    total_content_size = 0
    for content_type, data in content_types.items():
        content_size_mean = get_value(data['contentSize'], 'mean')
        results['totalContentSize'][content_type] = content_size_mean if content_size_mean != "N/A" else 0
        total_content_size += results['totalContentSize'][content_type]
    if results['totalContentSize']['total'] == "N/A":
        results['totalContentSize']['total'] = total_content_size
    return results

def create_metrics_to_json_result(parsed_json, verify_browsertime_json, verify_pagexray_json):
    metrics = parsed_json['performance_evaluation']['metrics']
    results = {}
    content_types = verify_pagexray_json["contentTypes"]

    for metric in metrics:
        if metric in ['requests', 'contentSize']:
            results.update(handle_requests_and_content_size(metric, verify_pagexray_json, content_types))
        else:
            results[metric] = get_metric_value(metric, verify_browsertime_json, verify_pagexray_json)

    return results

def create_metrics_to_detailed_result(parsed_json, verify_browsertime_runs):
    metrics = parsed_json['performance_evaluation']['metrics']
    interations = verify_browsertime_runs['browsertime_runs']

    detailed_metrics_results = []
    interation_index = 1

    for interation in interations:
        key = list(interation.keys())[0]
        value = interation[key]
        metrics_results = {}

        for metric in metrics:
            if metric == 'firstContentfulPaint':
                metrics_results["firstContentfulPaint"] = value['har']['log']['pages'][0]['pageTimings']['_firstContentfulPaint']
            elif metric == 'totalBlockingTime':
                if '_googleWebVitals' not in value['har']['log']['pages'][0]:
                    metrics_results['totalBlockingTime'] = "N/A"
                else:
                    metrics_results['totalBlockingTime'] = value['har']['log']['pages'][0]['_googleWebVitals']['totalBlockingTime']
            elif metric == 'largestContentfulPaint':
                if '_largestContentfulPaint' not in value['har']['log']['pages'][0]['pageTimings']:
                    metrics_results['largestContentfulPaint'] = "N/A"
                else:
                    metrics_results['largestContentfulPaint'] = value['har']['log']['pages'][0]['pageTimings']['_largestContentfulPaint']
            elif metric == 'cumulativeLayoutShift':
                if '_googleWebVitals' not in value['har']['log']['pages'][0]:
                    metrics_results['cumulativeLayoutShift'] = "N/A"
                else:
                    metrics_results['cumulativeLayoutShift'] = value['har']['log']['pages'][0]['_googleWebVitals']['cumulativeLayoutShift']
            elif metric == 'pageLoadTime':
                metrics_results["pageLoadTime"] = value['timings']['pageTimings']['pageLoadTime']
            elif metric == 'ttfb':
                if '_googleWebVitals' not in value['har']['log']['pages'][0]:
                    metrics_results['ttfb'] = value['timings']['navigationTiming']['responseStart']
                else:
                    metrics_results['ttfb'] = value['har']['log']['pages'][0]['_googleWebVitals']['ttfb']
            elif metric == 'maxPotentialFid':
                if 'cpu' not in value:
                    metrics_results['maxPotentialFid'] = "N/A"
                else:
                    metrics_results['maxPotentialFid'] = value['cpu']['longTasks']['maxPotentialFid']

        result = {}
        result['interation_run'] = interation_index
        result['metricsResults'] = metrics_results
        detailed_metrics_results.append(result)
        interation_index += 1

    json_result = {'detailedMetricsResults': detailed_metrics_results}
    # print(json_result)
    return detailed_metrics_results