from .querycomponent import QueryComponent
from indexing import Index, Posting
from text.advancedtokenprocessor import AdvancedTokenProcessor
from querying import querycomponent, NotQuery

class AndQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        # please don't rename the "components" field.
        self.components = components

    def get_postings(self, index : Index) -> list[Posting]:
        atp = AdvancedTokenProcessor()
        result = []
        # TODO: program the merge for an AndQuery, by gathering the postings of the composed QueryComponents and
		# intersecting the resulting postings.
        p1 = index.get_postings(atp.normalize_type({str(self.components[0])})[0])
        i = 1
        while (i < len(self.components)):
            result = []
            if type(self.components[i]) is NotQuery:
                p2 = self.components[i].get_postings(index)
                p1_p = 0
                p2_p = 0
                while (p1_p < len(p1) and p2_p < len(p2)):
                    if p1[p1_p].doc_id < p2[p2_p].doc_id:
                        result.append(p1[p1_p])
                        p1_p += 1
                    else:
                        p2_p += 1
            else:
                p2 = index.get_postings(atp.normalize_type({str(self.components[i])})[0])
                p1_p = 0
                p2_p = 0
                while (p1_p < len(p1) and p2_p < len(p2)):
                    if p1[p1_p].doc_id == p2[p2_p].doc_id:
                        result.append(p1[p1_p])
                        p1_p += 1
                        p2_p += 1
                    elif p1[p1_p].doc_id < p2[p2_p].doc_id:
                        p1_p += 1
                    else:
                        p2_p += 1
            p1 = result
            i += 1
        return result

    def __str__(self):
        return " AND ".join(map(str, self.components))