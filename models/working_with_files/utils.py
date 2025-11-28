import os
import logging
from typing import Optional, Tuple

log = logging.getLogger(__name__)


def find_file(path_of_dir: str, file_name: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Универсальная проверка существования файла.

    Если file_name не указано — path_of_dir считается ПРЯМЫМ путём к файлу.
    Если file_name указано — проверяется, существует ли этот файл внутри директории path_of_dir.

    Возвращает:
        (True, путь_к_файлу) — если файл найден
        (False, None) — если файл не найден или недоступен
    """
    try:
        # Формируем путь
        if file_name:
            target_path = os.path.join(path_of_dir, file_name)
        else:
            target_path = path_of_dir

        # Проверяем наличие
        exists = os.path.isfile(target_path)
        log.debug(f"Проверка пути: {target_path} → {'найден' if exists else 'не найден'}")

        if exists:
            return True, target_path
        return False, None

    except FileNotFoundError:
        log.error(f"Путь {path_of_dir} не найден.")
        return False, None
    except PermissionError:
        log.error(f"Нет прав доступа к {path_of_dir}.")
        return False, None
    except Exception as e:
        log.error(f"Ошибка при проверке файла {file_name or path_of_dir}: {e}")
        return False, None



from pathlib import Path
import sys
import os

def get_base_dir() -> Path:
    """
    Возвращает базовую директорию проекта.

    Если программа запущена как .exe — возвращает папку, где находится .exe.
    Если запущена как .py — возвращает корень проекта (родитель текущего файла).
    """
    if getattr(sys, 'frozen', False):  # Если это сборка через PyInstaller
        return Path(sys.executable).parent
    else:
        # Путь до файла, из которого импортируется эта функция
        return Path(__file__).resolve().parent.parent  # т.е. корень проекта


if __name__ == "__main__":
    import config_log

    config_log.config_logging(logging.DEBUG)
    print(find_file(
        '//192.168.0.253/Obmen/5.АУП/Евгений/Стройка Евразия/Объекты/Объект Лицей/Фото видео', '20251013_102616.jpg'))
