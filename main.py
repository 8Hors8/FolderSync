import logging
import json

import config_log
from json_tools.creation_json import check_json_file

config_log.config_logging(logging.DEBUG)

log = logging.getLogger(__name__)


def start(path_folder_collection: str, path_folder_tracking: str = None):
    root = []
    check_json_file()
    # if path_folder_tracking is None:
    #     root.append(scan_folder(path_folder_collection,flag_collection=True))
    # else:
    #     root.append(scan_folder(path_folder_collection, flag_collection=True))
    #     root.append(scan_folder(path_folder_tracking))


    log.debug(json.dumps(root, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    path1 = r'C:\Users\ПТО\Desktop\тест контейнер'
    path2 = r'C:\Users\ПТО\Desktop\Сервер тест'
    start(path1,path2)
