import logging
from typing import Any, Dict, Optional, Union


from models.json_templates import COLLECTION_TEMPLATE, TRACKED_TEMPLATE, INDEX_TEMPLATE
from models.scanning_folder.scan_folderes import scan_folder

log = logging.getLogger(__name__)


class ScanManager:
    def __init__(self, data: Dict[str, Any], path: str = None, flag_collection: bool = False) -> Dict[str, Any]:
        self.data = data
        self.index = data['index']
        self.path = path
        self.flag_collection = flag_collection
        self.COLLECTION_TEMPLATE=COLLECTION_TEMPLATE
        self.TRACKED_TEMPLATE=TRACKED_TEMPLATE
        self.INDEX_TEMPLATE=INDEX_TEMPLATE

    def tree_construction(self):
        if self.flag_collection:
            pass
        pass
