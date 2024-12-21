import os

def get_file_path():
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
    return os.path.abspath(os.path.join(parent_dir, "updated_quotes.json"))