from bisect import bisect_left
from decimal import InvalidOperation
from pydoc import doc
from typing import Iterable
from .postings import Posting
from .index import Index


class InvertedIndex(Index):

    def __init__(self, vocab : Iterable[str]):
        self.vocabulary = list(vocab)
        self.vocabulary.sort()
        self._index = {}

    def addTerm(self, term : str, doc_id : int):
        appearance = {term : [Posting(doc_id)]}
        if (self._index.get(term) == None):
            self._index.update(appearance)
        elif doc_id > self._index.get(term)[-1].doc_id:
            self._index[term].append(Posting(doc_id))


    def getPostings(self, term : str) -> Iterable[Posting]:
        """Returns a list of Postings for all documents that contain the given term."""
        return self._index.get(term)
            
    
    def getVocabulary(self) -> Iterable[str]:
        return self.vocabulary
    