import os


def get_defaults_path():
    """Get the full path to the defaults.txt file"""
    from pkg_resources import resource_filename

    fn = resource_filename("openff.units", os.path.join("data", "defaults.txt"))

    return fn
