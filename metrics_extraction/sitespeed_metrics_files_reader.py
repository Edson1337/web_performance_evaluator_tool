import json
import os
from pathlib import Path
import re
from lxml import etree, html

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def read_browsertime_json(results, browsertime_file):
    browsertime_json_path = Path(results) / browsertime_file
    return read_json_file(browsertime_json_path)

def read_pagexray_json(results, pagexray_file):
    pagexray_json_path = Path(results) / pagexray_file
    return read_json_file(pagexray_json_path)

def read_infos_json(infos, har_file):
    infos_har_path = Path(infos) / har_file
    return read_json_file(infos_har_path)

def read_browsertime_run(infos):
    browsertime_runs = []
    for file in os.listdir(infos):
        if re.match(r'browsertime\.run-\d+\.json$', file):
            run_file_path = Path(infos) / file
            data = read_json_file(run_file_path)
            browsertime_runs.append({file: data})
    return {'browsertime_runs': browsertime_runs}

def read_index_html(path_result_sitespeed, html_file):
    path_html = Path(path_result_sitespeed) / html_file
    print("HTML file: ", path_html)
    try:
        with open(path_html, 'r', encoding='utf-8') as file:
            html_content = file.read()
        doc = html.fromstring(html_content)
        p_element = doc.cssselect('p')[0] if doc.cssselect('p') else None
        if not p_element:
            print("Element <p> not found")
            return None
        extracted_text = p_element.text_content()
        match = re.search(r'\busing\s+(\w+)\s+\(', extracted_text)
        if not match or not match.group(1):
            print("Text in brackets not found")
            return None
        browser_name = match.group(1)
        print("browser: ", browser_name)
        return browser_name
    except Exception as error:
        print("Error reading HTML file: ", error)
        return None