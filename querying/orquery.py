from .querycomponent import QueryComponent
from indexing import Index, Posting

from querying import querycomponent, AndQuery

class OrQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    def get_postings(self, index : Index) -> list[Posting]:
        result = []
        # TODO: program the merge for an OrQuery, by gathering the postings of the composed QueryComponents and
		# merging the resulting postings.
        if type(self.components[0]) == AndQuery:
            p1 = self.components[0].get_postings(index)
        else:
            p1 = index.get_postings(str(self.components[0]))
        i = 1
        while (i < len(self.components)):
            result = []
            p2 = index.get_postings(str(self.components[i]))
            p1_p = 0
            p2_p = 0
            while (p1_p < len(p1) and p2_p < len(p2)):
                if p1[p1_p].doc_id == p2[p2_p].doc_id:
                    result.append(p1[p1_p])
                    p1_p += 1
                    p2_p += 1
                elif p1[p1_p].doc_id < p2[p2_p].doc_id:
                    result.append(p1[p1_p])
                    p1_p += 1
                else:
                    result.append(p2[p2_p])
                    p2_p += 1
            p1 = result
            i += 1
        return result

    def __str__(self):
        return "(" + " OR ".join(map(str, self.components)) + ")"