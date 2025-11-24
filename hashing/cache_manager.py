
from hashing.util import folder_hash, file_hash


def hash_file_folder(path, type_dir: str):
    if type_dir == "folder":
        result = folder_hash(path)

    else:
        result = file_hash(path)
    return result