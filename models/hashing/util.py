import hashlib
import os
import logging

log = logging.getLogger(__name__)



def folder_hash(path: str, algo="sha256"):
    log.debug("hashing folder %s", path)
    h = hashlib.new(algo)
    for root, _, files in os.walk(path):
        for file in sorted(files):  # сортируем, чтобы порядок не влиял
            filepath = os.path.join(root, file)
            h.update(file_hash(filepath, algo).encode())
    return h.hexdigest()

def file_hash(path: str, algo="sha256"):
    log.debug("hashing file %s", path)
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):  # читаем кусками
            h.update(chunk)
    return h.hexdigest()

