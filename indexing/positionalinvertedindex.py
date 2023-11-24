from bisect import bisect_left
from decimal import InvalidOperation
from pydoc import doc
from typing import Iterable, Dict
from .postings import Posting
from .index import Index


class PositionalInvertedIndex(Index):

    def __init__(self):
        #constructs an empty vocabulary list
        # self.vocabulary = {}
        self._index : Dict[str, list[Posting]] = {}


    def add_term(self, term : str, doc_id : int, pos : int):
        """
        pList = self.vocabulary.get(term)
        if pList == None:
            self.vocabulary[term] = []
            self.vocabulary[term].append(Posting(doc_id, [pos]))
        else:
            idx = 0
            for p in pList:
                if doc_id == p.doc_id:
                    self.vocabulary[term][idx].position.append(pos)
                    return
                else:
                    idx += 1
            self.vocabulary[term].append(Posting(doc_id, [pos]))
        """
        postings = self._index.get(term, None)
        if postings is not None:
            last_post = postings[-1]
            if last_post.doc_id != doc_id:
                postings.append(Posting(doc_id, pos))
            else:
                last_post.position.append(pos)
        else:
            self._index[term] = [Posting(doc_id, pos)]
        
    #if the posting does not exist, returns an empty list, then returns the value
    def get_postings(self, term: str) -> Iterable[Posting]:
        """
        if self.vocabulary.get(term) == None:
            return []
        return self.vocabulary.get(term)
        """
        return self._index.get(term, [])
    
    #returns a sorted list of the keys
    def get_Vocabulary(self) -> Iterable[str]:
        return sorted(self._index.keys())
