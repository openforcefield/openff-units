from openff.utilities import get_data_file_path

def get_defaults_path() -> str:
    """Get the full path to the defaults.txt file"""
    return get_data_file_path("data/defaults.txt", "openff.units")
