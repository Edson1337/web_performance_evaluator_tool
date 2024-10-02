from pathlib import Path

root_folder_path = Path("temp_scenario_settings").resolve()
config_folder_path = root_folder_path / "configs"

def delete_sitespeed_results(site_speed_result_path):
    delete_folder(site_speed_result_path)
    print(f"{site_speed_result_path} Deleted recursively.")

def delete_folder(folder_path):
    folder_path = Path(folder_path)
    for item in folder_path.iterdir():
        if item.is_dir():
            delete_folder(item)
        else:
            item.unlink()
    folder_path.rmdir()