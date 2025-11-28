import logging

import config_log
from managers.json_state_manager import JsonStateManager
from managers.scan_manager import ScanManager


config_log.config_logging(logging.DEBUG)
# config_log.config_logging()

log = logging.getLogger(__name__)


class RanSync:
    def __init__(self):
        self.json_manager = JsonStateManager()
        self.skan = ScanManager(self.json_manager)
    def start(self):
        pass




if __name__ == '__main__':
    path1 = r'C:\Users\ПТО\Desktop\тест контейнер'
    path2 = r'C:\Users\ПТО\Desktop\Сервер тест'
    start_prod = RanSync()

