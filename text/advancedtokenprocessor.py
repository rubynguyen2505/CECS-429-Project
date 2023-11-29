from .tokenprocessor import TokenProcessor
from porter2stemmer import Porter2Stemmer
import re

class AdvancedTokenProcessor(TokenProcessor):
    """A AdvancedTokenProcessor creates terms from tokens by removing all non-alphanumeric characters 
    from the token, and converting it to all lowercase."""
    whitespace_re = re.compile(r"^\W+|\W+$")
    
    def process_token(self, token : str) -> set[str]:
        result = []
        result1 = []
        if (token is not None):
            if "-" in token:
                result = re.split("-", token)
                result.append(re.sub("-", "", token))
            else:
                result.append(token)

        # print(type(result))
        if (result is not None):
            for r in result:
                # Remove non-alphanumeric characters from the beginning and end of the token, but not the middle
                r = re.sub(self.whitespace_re, "", r)
                # Remove all apostrophes or quotation marks (single or double quotes) from anywhere in the token.
                r = re.sub('"', '', r)
                r = re.sub("'", "", r)
                # Convert the token to lowercase
                r = r.lower()
                # print(r)
                result1.append(r)
        if (result1 is not None):
            return result1

    def normalize_type(self, type : {str}) -> {str}:
        # Stem using a "Porter2 Stemmer".
        list_terms = []
        stemmer = Porter2Stemmer()
        for t in type:
            t = stemmer.stem(t)
            list_terms.append(t)
        return list_terms