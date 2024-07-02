from utils.dir_formater import create_path_to_read_infos, create_path_to_read_results
from metrics_extraction.sitespeed_metrics_files_reader import read_browsertime_json, read_pagexray_json, read_infos_json, read_browsertime_run, read_index_html
from metrics_extraction.performance_metrics import create_metrics_to_json_result, create_metrics_to_detailed_result
import re

def create_scenery_name(verify_infos_har, verify_html):
    browser_name = verify_html.lower()
    connectivity_type = verify_infos_har['log']['pages'][0]['_meta']['connectivity']
    match = re.search(r"Emulated (.+)", verify_infos_har['log']['browser']['name'])
    device_name = match.group(1) if match else "desktop"
    scenery_name = f"{browser_name}_{connectivity_type}_{device_name.replace(' ', '').lower()}"
    return scenery_name

def create_summarized_result(parsed_json, path_result_site_speed):
    infos = create_path_to_read_infos(path_result_site_speed)
    # print(infos)
    results = create_path_to_read_results(path_result_site_speed)

    browsertime_file = 'browsertime.summary-total.json'
    pagexray_file = 'pagexray.summary-total.json'
    har_file = 'browsertime.har'
    html_file = 'index.html'

    verify_infos_har = read_infos_json(infos, har_file)
    verify_html = read_index_html(path_result_site_speed, html_file)
    # print(f"HTML: {verify_html}")
    verify_browsertime_json = read_browsertime_json(results, browsertime_file)
    verify_pagexray_json = read_pagexray_json(results, pagexray_file)
    verify_browsertime_runs = read_browsertime_run(infos)

    scenery_name = create_scenery_name(verify_infos_har, verify_html)
    metrics_results = create_metrics_to_json_result(parsed_json, verify_browsertime_json, verify_pagexray_json)
    detailed_metrics_results = create_metrics_to_detailed_result(parsed_json, verify_browsertime_runs)

    summarized_result = {
        'scenario_name': scenery_name,
        'metricsResults': metrics_results,
        'detailedMetricsResults': detailed_metrics_results
    }

    return summarized_result