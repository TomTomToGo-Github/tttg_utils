## built-in modules
from pathlib import Path


def ensure_folder_structure(folders_dict=None):
    nested_paths = paths_from_nested_dict(folders_dict)
    for path_dir in nested_paths:
        if not path_dir.is_dir():
            path_dir.mkdir(parents=True)

def paths_from_nested_dict(self, paths_dict, nested_paths=None):
    if nested_paths is None:
        nested_paths = [Path("")]
    for key, value in paths_dict.items():
        nested_paths[-1] = nested_paths[-1] / key
        if isinstance(value, dict):
            self.paths_from_nested_dict(value, nested_paths)
        elif value == "":
            nested_paths.append(nested_paths[-1].parent)
    nested_paths[-1] = nested_paths[-1].parent
    return nested_paths
