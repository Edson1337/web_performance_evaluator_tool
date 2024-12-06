from utils.dir_formater import create_path_to_read_pages_content, create_path_to_read_results
from metrics_extraction.sitespeed_metrics_files_reader import ResultsReader
from metrics_extraction.performance_metrics import create_metrics_to_json_result, create_metrics_to_detailed_result, create_metrics_to_statistical_result
import re

def create_scenery_name(verify_infos_har, verify_html):
    browser_name = verify_html.lower()
    connectivity_type = verify_infos_har['log']['pages'][0]['_meta']['connectivity']
    match = re.search(r"Emulated (.+)", verify_infos_har['log']['browser']['name'])
    device_name = match.group(1) if match else "desktop"
    scenery_name = f"{browser_name}_{connectivity_type}_{device_name.replace(' ', '').lower()}"
    return scenery_name

def create_summarized_result(parsed_json, path_result_sitespeed):
    infos = create_path_to_read_pages_content(path_result_sitespeed)
    results = create_path_to_read_results(path_result_sitespeed)

    reader = ResultsReader()

    browsertime_file = 'browsertime.summary-total.json'
    pagexray_file = 'pagexray.summary-total.json'
    har_file = 'browsertime.har'
    html_file = 'index.html'

    verify_infos_har = reader.read_infos_json(infos, har_file)
    verify_html = reader.read_index_html(path_result_sitespeed, html_file)
    # print(f"HTML: {verify_html}")
    verify_browsertime_json = reader.read_browsertime_json(results, browsertime_file)
    verify_pagexray_json = reader.read_pagexray_json(results, pagexray_file)
    verify_browsertime_runs = reader.read_browsertime_run(infos)

    scenario_name = create_scenery_name(verify_infos_har, verify_html)
    metrics_results = create_metrics_to_json_result(parsed_json, verify_browsertime_json, verify_pagexray_json)
    detailed_metrics_results = create_metrics_to_detailed_result(parsed_json, verify_browsertime_runs)

    if("-csr" or "_after") in parsed_json['performance_evaluation']['app_name']:
        print(f"Metrics: {parsed_json['performance_evaluation']['metrics']}")
        compare_file = 'compare.pageSummary.json'
        verify_compare_json = reader.read_compare_json(infos, compare_file)
        statistical_result = create_metrics_to_statistical_result(parsed_json, verify_compare_json)

        return {
            'scenario_name': scenario_name,
            'metricsResults': metrics_results,
            'detailedMetricsResults': detailed_metrics_results,
            'statisticalResult': statistical_result
        }

    summarized_result = {
        'scenario_name': scenario_name,
        'metricsResults': metrics_results,
        'detailedMetricsResults': detailed_metrics_results
    }

    return summarized_result

# def create_comparative_result(parsed_json, path_result_sitespeed):
#     infos = create_path_to_read_pages_content(path_result_sitespeed)

#     reader = ResultsReader()

#     compare_file = 'compare.pageSummary.json'
#     verify_compare_json = reader.read_compare_json(infos, compare_file)
#     statistical_result = create_metrics_to_statistical_result(parsed_json, verify_compare_json)

#     return {
#         'statisticalResult': statistical_result
#     }