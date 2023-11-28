from bisect import bisect_left
from decimal import InvalidOperation
from pydoc import doc
from typing import Iterable, Dict
from .postings import Posting
from .index import Index


class PositionalInvertedIndex(Index):

    def __init__(self):
        #constructs an empty vocabulary list
        self.vocabulary : Dict[str, list[Posting]] = {}
        # self._index : Dict[str, list[Posting]] = {}


    def add_term(self, term : str, doc_id : int, pos : int):
        
        pList = self.vocabulary.get(term)
        if pList is None:
            self.vocabulary[term] = [Posting(doc_id, pos)]
        else:
            lp = pList[-1]
            if doc_id == lp.doc_id:
                lp.position.append(pos)
            else:
                pList.append(Posting(doc_id, pos))
        

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
        """
        
    #if the posting does not exist, returns an empty list, then returns the value
    def get_postings(self, term: str) -> Iterable[Posting]:
        """
        if self.vocabulary.get(term) == None:
            return []
        return self.vocabulary.get(term)
        """
        return self.vocabulary.get(term, [])
    
    #returns a sorted list of the keys
    def get_Vocabulary(self) -> Iterable[str]:
        return sorted(self.vocabulary.keys())
