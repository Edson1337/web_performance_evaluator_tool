import os
import json
from result_summarization.summarized_results_assembler import create_summarized_result
import re
from result_summarization.summarized_results_file import create_file


sitespeed_result_path = os.path.normpath('sitespeed-result/')
root_folder_path = os.path.normpath("temp_scenario_settings/")
regex_pattern = r'^.*$'

def assemble_summarize_results(parsed_json):
    summarized_results = []

    sitespeed_results_files = os.listdir(sitespeed_result_path)

    matching_files = [f for f in sitespeed_results_files if re.match(regex_pattern, f)]

    for file_name in matching_files:
        file_path = os.path.join(sitespeed_result_path, file_name)
        inner_files = os.listdir(file_path)
        for file in inner_files:
            path_result_sitespeed = os.path.join(file_path, file)

            print(path_result_sitespeed)
            summarized_result = create_summarized_result(parsed_json, path_result_sitespeed)
            scenery_json_string = json.dumps(summarized_result)
            # print(scenery_json_string)

            summarized_results.append(summarized_result)
            # print(summarized_results)

        # print("summarizedResults certo: ", summarized_results)
        parsed_json['performance_evaluation']['scenarios'] = summarized_results

        print("parsed_json certo: ", parsed_json)
        create_file(parsed_json)