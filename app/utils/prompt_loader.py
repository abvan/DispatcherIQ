import yaml

def load_prompt(file_path: str):
    
    if len(file_path) == 0:
        raise ValueError("File path cannot be empty.")

    with open(file_path, "r") as f:
        return yaml.safe_load(f)