import logging, os


log = logging.getLogger(__name__)


def extract_formats(path: str) -> str:
    """Функция извлекает формат из пути.
    :param path: Путь к файлу.
    :return str (Строку с расширением файла '.text')
    """
    log.debug(f'Изъятия формата из {path}')
    _, ext = os.path.splitext(path)
    return ext.lower()



if __name__ == "__main__":

    print(extract_formats("/home/user/folder/Точечный рисунок.bmp"))