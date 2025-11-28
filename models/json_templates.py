import datetime
from copy import deepcopy
from typing import Any, Dict


COLLECTION_TEMPLATE: Dict[str, Any] = {
    "path": "",          # путь к коллекции
    "hash": "",          # общий хеш
    "last_scan": "",     # время последнего сканирования
    "children": []       # структура файлов/папок после сканирования
}


TRACKED_TEMPLATE: Dict[str, Any] = {
    "alias": "",         # имя папки
    "path": "",          # путь
    "enabled": True,
    "hash": "",
    "last_scan": "",
    "children": []       # структура сканирования
}
INDEX_TEMPLATE: Dict[str, Any] = {
    "type": "",
    "size": None,
    "modified": None,
    "hash": "",
    "belongs_to": "collection"
}



def create_initial_data() -> Dict[str, Any]:
    """
    Создаёт минимально необходимую структуру JSON,
    подходящую для текущей версии проекта.
    """
    return {
        "meta": {
            "version": 1,
            "created": datetime.datetime.now().isoformat(),
        },

        # Основная коллекция
        "collection": {
            "path_collection": "",
            "last_scan": "",
            "children": []
        },

        "index":{

        },

        # Отслеживаемые папки — список элементов TRACKED_TEMPLATE
        "tracked": [],

        # Файлы, которые вызвали конфликты
        "conflicts": [],

        # Простейший системный кеш
        "system": {
            "total_files": 0,
            "last_update": ""
        }
    }
