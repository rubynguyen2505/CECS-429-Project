from indexing.postings import Posting
from text.advancedtokenprocessor import AdvancedTokenProcessor
from .querycomponent import QueryComponent

class TermLiteral(QueryComponent):
    """
    A TermLiteral represents a single term in a subquery.
    """

    def __init__(self, term : str):
        self.term = term

    def get_postings(self, index) -> list[Posting]:
        atp = AdvancedTokenProcessor()
        self.term = atp.normalize_type({self.term})
        return index.get_postings(self.term[0])

    def __str__(self) -> str:
        return self.term