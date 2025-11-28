"""
creation_json
================================

Утилиты для создания / проверки / чтения основного JSON-файла состояния
(например, "sync_state.json") используемого программой синхронизации.

Задачи модуля:
- проверить, существует ли JSON-файл в указанной директории (или по полному пути);
- при отсутствии — создать новый файл по шаблону (json_templates.create_initial_data);
- безопасно загрузить JSON в виде словаря;
- логировать ошибки чтения/записи и возвращать готовый словарь (всегда возвращаем dict,
  чтобы вызывающий код мог спокойно работать с результатом).

Зависимости:
- working_with_files.utils.find_file(path, file_name) -> (bool, Optional[str])
- working_with_files.utils.get_base_dir() -> Path
- config_project.JSON_FILE_NAME (имя файла конфигурации)
- json_templates.create_initial_data() -> dict (шаблон для создания файла)
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Union

from models.working_with_files.utils import find_file  # ожидается: (bool, Optional[str])
from models.working_with_files.utils import get_base_dir  # ожидается: Path
from config_project import JSON_FILE_NAME
from models.json_tools.json_templates_2 import create_initial_data # выбрать нужный шаблон

log = logging.getLogger(__name__)


def check_json_file(path_file_json: Optional[Union[str, Path]] = None) -> Dict:
    """
    Проверяет наличие и корректность JSON-файла конфигурации и возвращает его содержимое.

    Поведение:
    - Если path_file_json не указан: используется текущая рабочая директория (Path.cwd()).
    - Если path_file_json указывает на файл или директорию, функция корректно определит
      путь к JSON и попытается его открыть.
    - Если файл отсутствует — создаётся новый файл по шаблону (create_initial_data()).
    - Если файл присутствует, но чтение/декодирование выдаёт ошибку — создаётся новый файл.
    - Функция всегда возвращает словарь (dict). В случае ошибки при создании возвращается
      пустой шаблон (create_initial_data()).

    :param path_file_json: путь к директории или к файлу (опционально)
    :return: dict — содержимое JSON (схема соответствует create_initial_data())
    """
    # Нормализация входного параметра в Path
    base = Path(path_file_json) if path_file_json is not None else get_base_dir()

    # Если нам передали путь прямо на файл (или путь, оканчивающийся на JSON_FILE_NAME),
    # попробуем использовать его как целевой файл.
    if base.is_file() or str(base).endswith(JSON_FILE_NAME):
        json_path = base if base.is_file() else Path(base)
        # если файл существует — пробуем прочитать
        if json_path.exists():
            try:
                return reading_json_file(json_path)
            except Exception:
                log.warning("Файл найден, но не удалось корректно прочитать. Пересоздаём файл.")
                created_path = creation_setting_json(json_path.parent)
                return reading_json_file(created_path)
        else:
            # файл не существует — создаём в той же директории
            created_path = creation_setting_json(json_path.parent)
            return reading_json_file(created_path)

    # Если base — директория или неизвестно, ищем JSON внутри директории
    directory = base if base.is_dir() else base.parent
    found, found_path = find_file(str(directory), JSON_FILE_NAME)

    if found and found_path:
        # найден путь к JSON — пытаемся загрузить
        try:
            return reading_json_file(found_path)
        except Exception:
            log.warning("Файл JSON найден, но повреждён или не читается. Пересоздаём новый файл.")
            created_path = creation_setting_json(directory)
            return reading_json_file(created_path)
    else:
        # не найден — создаём новый
        log.info(f"Файл {JSON_FILE_NAME} не найден в {directory}. Создаём новый.")
        created_path = creation_setting_json(directory)
        return reading_json_file(created_path)


def creation_setting_json(base_dir: Optional[Union[str, Path]] = None) -> Path:
    """
    Создаёт JSON-файл конфигурации с начальными настройками и возвращает путь к созданному файлу.

    :param base_dir: директория, в которой создать JSON (если None — используется cwd)
    :return: Path — полный путь к созданному файлу
    """
    base = Path(base_dir) if base_dir is not None else Path.cwd()
    base.mkdir(parents=True, exist_ok=True)

    initial_data = create_initial_data()  # вызываем функцию, чтобы получить структуру

    json_path = base / JSON_FILE_NAME
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=4)
        log.info(f"Файл {JSON_FILE_NAME} успешно создан: {json_path}")
    except Exception as e:
        log.error(f"Ошибка при создании файла {json_path}: {e}")
        # В случае ошибки всё равно возвращаем путь (или можно вернуть None)
    return json_path


def reading_json_file(path_json: Union[str, Path]) -> Dict:
    """
    Прочитать JSON-файл и вернуть его содержимое в виде словаря.

    Функция бросает исключение в случае серьёзной ошибки чтения/декодирования.
    Вызывающий код (check_json_file) обрабатывает исключения и при необходимости
    пересоздаёт файл.

    :param path_json: путь к JSON-файлу
    :return: dict — содержимое JSON
    :raises: json.JSONDecodeError, OSError и т.д.
    """
    p = Path(path_json)
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    log.info(f"Файл состояния успешно загружен: {p}")
    log.debug(f"Содержимое {p}:\n{json.dumps(data, ensure_ascii=False, indent=2)}")
    return data


# Простая CLI-проверка при запуске модуля напрямую
if __name__ == "__main__":
    import config_log

    config_log.config_logging(logging.DEBUG)

    # Попробуем загрузить или создать JSON в текущей директории модуля
    result = check_json_file(Path.cwd())
    print("Результат загрузки (верхний уровень ключей):", list(result.keys()))
