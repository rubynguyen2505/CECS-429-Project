import json
from pathlib import Path
from typing import Iterable
from .document import Document

class JsonFileDocument(Document):
    """
    Represents a document that is saved as a simple text file in the local file system.
    """
    def __init__(self, id : int, path : Path):
        super().__init__(id)
        self.path = path

    @property
    def title(self) -> str:
        return json.load(open(self.path, encoding = 'utf8'))['title']

    # returns TextIOWrapper
    def get_content(self) -> Iterable[str]:
        return json.load(open(self.path, encoding = 'utf8'))['body']

    @staticmethod
    def load_from(abs_path : Path, doc_id : int) -> 'JsonFileDocument' :
        """A factory method to create a JsonFileDocument around the given file path."""
        return JsonFileDocument(doc_id, abs_path)