class Posting:
    """A Posting encapulates a document ID associated with a search query component."""
    def __init__(self, doc_id : int, position : []):
        self.doc_id = doc_id
        self.position = position
