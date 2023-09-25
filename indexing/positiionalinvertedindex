from bisect import bisect_left
from decimal import InvalidOperation
from pydoc import doc
from typing import Iterable
from .postings import Posting
from .index import Index


class PositionalInvertedIndex(Index):

    def __init__(self, vocab : Iterable[str]):
        #constructs an empty vocabulary list
        self.vocabulary = {}

    def add_term(self, term : str, doc_id : int):
        #if pList does not exist, clears list, then appends the doc_id as a posting object
        pList = self.vocabulary.get(term)
        if pList == None:
            self.vocabulary[term] = []
            self.vocabulary[term].append(Posting(doc_id))
        #if the value of the last element of pList is not the same as the doc_id, then append that doc_id as a posting object
        elif pList[-1].doc_id != doc_id:
            self.vocabulary[term].append(Posting(doc_id))
        
    #if the posting does not exist, returns an empty list, then returns the value
    def get_postings(self, term: str) -> Iterable[Posting]:
        if self.vocabulary.get(term) == None:
            return []
        return self.vocabulary.get(term)
        
    #returns a sorted list of the keys
    def get_Vocabulary(self) -> Iterable[str]:
        return sorted(self.vocabulary.keys())
