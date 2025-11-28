"""
json_state_manager.py
"""
import logging
import json
from pathlib import Path
from typing import Optional

from models.json_tools.creation_json import check_json_file

log = logging.getLogger(__name__)


class JsonStateManager:
    """
    Управляет состоянием JSON-файла:
    - создаёт при первом запуске;
    - загружает/сохраняет изменения;
    - даёт доступ к секциям (collection, tracked, conflicts и т.д.).
    """

    def __init__(self, file_path: Optional[str]=None):
        self.file_path = file_path
        self.data = {}
        self.load_or_create()

    def load_or_create(self):
        """Если файл существует — загрузить, иначе создать шаблонный."""
        self.data = check_json_file(self.file_path)

    def save(self):
        """Сохраняет текущие данные в JSON."""
        try:
            with open(Path(self.file_path), "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            log.info(f"JSON состояние обновлено: {self.file_path}")
        except Exception as e:
            log.error(f"Ошибка сохранения JSON: {e}")

    def update_tracked(self, path, new_data):
        """Обновляет данные конкретной отслеживаемой папки."""
        tracked = self.data.get("tracked", {})

        tracked[path] = new_data
        self.data["tracked"] = tracked

        self.save()
