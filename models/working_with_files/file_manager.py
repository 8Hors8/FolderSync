import os
import shutil
import hashlib


class FileManager:
    """
    Управляет физическими файлами на диске.
    Отвечает за копирование, удаление, замену и сравнение.
    """

    @staticmethod
    def ensure_dir_exists(path: str):
        """Создаёт директорию, если она отсутствует."""
        os.makedirs(os.path.dirname(path), exist_ok=True)

    @staticmethod
    def copy_file(src: str, dst: str):
        """Копирует файл с сохранением метаданных."""
        FileManager.ensure_dir_exists(dst)
        shutil.copy2(src, dst)

    @staticmethod
    def replace_file(src: str, dst: str):
        """Заменяет существующий файл новым."""
        FileManager.ensure_dir_exists(dst)
        os.replace(src, dst)

    @staticmethod
    def delete_file(path: str):
        """Удаляет файл, если он существует."""
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def calculate_hash(path: str, algorithm="sha256"):
        """Вычисляет хэш файла."""
        if not os.path.exists(path):
            return None

        hash_func = hashlib.new(algorithm)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    @staticmethod
    def files_are_equal(path1: str, path2: str) -> bool:
        """Сравнивает два файла по хэшу."""
        return FileManager.calculate_hash(path1) == FileManager.calculate_hash(path2)
