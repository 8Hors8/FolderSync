"""
Модуль настройки логирования для приложения.

Содержит функцию config_logging(level), которая конфигурирует базовое логирование
с заданным уровнем и форматом вывода.

Использование:
    import logging_config
    logging_config.config_logging(logging.DEBUG)  # установить уровень логирования DEBUG

Формат сообщения лога:
    [ГГГГ-ММ-ДД ЧЧ:ММ:СС.МСС] <модуль>:<строка> <уровень> - <сообщение>

По умолчанию уровень логирования — INFO.
"""


import logging

def config_logging(level=logging.INFO):
    """
        Настройка логирования для приложения.
        :param level: Уровень логирования. По умолчанию - INFO.
    """
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)7s - %(message)s"

    )