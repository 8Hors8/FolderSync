
import logging




log = logging.getLogger(__name__)


class ScanManager:
    def __init__(self, data):
        self.data = data
        self.index = data['index']



