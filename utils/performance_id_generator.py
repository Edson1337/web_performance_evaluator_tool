from datetime import datetime

def generate_performance_test_id(parsed_json: dict):
    
    parsed_json['performance_evaluation']['performance_evaluation_id'] = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    return parsed_json