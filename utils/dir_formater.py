import os
from pathlib import Path

def create_path_to_read_pages_content(file):
    file_path = Path(file)
    pages_path = Path('pages')
    # print(pages_path)
    sitespeed_results_path = file_path / pages_path
    # print(sitespeed_results_path)
    infos_path = find_data_folder(sitespeed_results_path)
    infos_folder = f"{infos_path}"
    return infos_folder

def create_path_to_read_results(file):
    file_path = Path(file)
    data_folder = Path('data')
    results_folder = file_path / data_folder
    return results_folder

def find_data_folder(starting_directory):
    for root, dirs, files in os.walk(starting_directory):
        if 'data' in dirs:
            return Path(root).joinpath('data')
    return None