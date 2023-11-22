from indexing.postings import Posting
from .querycomponent import QueryComponent

class PhraseLiteral(QueryComponent):
    """
    Represents a phrase literal consisting of one or more terms that must occur in sequence.
    """

    def __init__(self, terms : list[QueryComponent]):
        self.literals = terms

    def get_postings(self, index) -> list[Posting]:
        result = []
        # TODO: program this method. Retrieve the postings for the individual literals in the phrase,
		# and positional merge them together.
        p1 = index.get_postings(str(self.components[0]))
        i = 1
        k = 1
        while (i < len(self.components)):
            result = []
            p2 = index.get_postings(str(self.components[i]))
            p1_p = 0
            p2_p = 0
            while (p1_p < len(p1) and p2_p < len(p2)):
                if p1[p1_p].doc_id == p2[p2_p].doc_id:
                    p1_pp = 0
                    p2_pp = 0
                    while (p1_pp < len(p1[p1_p].postings) and p2_pp < len(p2[p2_p].postings)):
                        if (p1[p1_p].postings[p1_pp] < p2[p2_p].postings[p2_pp]):
                            if (p1[p1_p].postings[p1_pp] == p2[p2_p].postings[p2_pp] - k):
                                result.append(p1[p1_p])
                                break
                            else:
                                p1_pp += 1
                        else:
                            p2_pp += 1
                    p1_p += 1
                    p2_p += 1
                elif p1[p1_p].doc_id < p2[p2_p].doc_id:
                    p1_p += 1
                else:
                    p2_p += 1
            p1 = result
            i += 1
            k += 1
        return result

    def __str__(self) -> str:
        return '"' + " ".join(map(str, self.literals)) + '"'