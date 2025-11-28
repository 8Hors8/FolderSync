import os
import logging

from models.hashing import hash_file_folder
from .utils import extract_formats

log = logging.getLogger(__name__)


def scan_folder(path: str, flag_collection: bool = False) -> dict:
    result = {
        "type": "folder",
        "name": os.path.basename(path),
        "path": os.path.abspath(path),
        "flag_collection": flag_collection,
        "hash_folder": hash_file_folder(path, "folder"),
        "allowed_formats": set(),
        "children": []
    }

    try:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file():
                    result["allowed_formats"].add(extract_formats(entry.path))
                    stat = entry.stat()
                    result["children"].append({
                        "type": "file",
                        "name": entry.name,
                        "path": entry.path,
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "inode": getattr(stat, "st_ino", None)
                    })
                elif entry.is_dir():
                    result["children"].append(scan_folder(entry.path, flag_collection))

        # в конце конвертируем set → list, чтобы сериализация в JSON прошла
        result["allowed_formats"] = list(result["allowed_formats"])

    except Exception as e:
        log.error(f"Ошибка при сканировании {path}: {e}")

    return result
