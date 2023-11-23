#Zach Brown
#025473992
#9/4/23

from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, TermDocumentIndex, PositionalInvertedIndex, DiskIndexWriter, DiskPositionalIndex
from text import BasicTokenProcessor, AdvancedTokenProcessor, englishtokenstream
from querying import BooleanQueryParser, AndQuery, OrQuery

"""This basic program builds a term-document matrix over the .txt files in 
the same directory as this file."""

def index_corpus(corpus : DocumentCorpus) -> Index:
    
    token_processor = AdvancedTokenProcessor()
    vocabulary = set()
    
    for d in corpus:
        print(f"Found document {d.title}")
        # TODO:
        #   Tokenize the document's content by creating an EnglishTokenStream around the document's .content()
        tokens = englishtokenstream.EnglishTokenStream(d.get_content())
        #   Iterate through the token stream, processing each with token_processor's process_token method.
        for token in tokens:
            for x in token.split(" "):
                tok = x.strip()
                if (len(tok) > 0):
                    list_terms = token_processor.process_token(tok)
                    #   Add the processed token (a "term") to the vocabulary set.
                    if (list_terms is not None):
                        for t in list_terms:
                            vocabulary.add(t)


    InvInd = PositionalInvertedIndex(vocabulary)

    # Iterate through the documents in the corpus:
    for d in corpus:
        pos = 0
    #   Tokenize each document's content, again.
        tokens = englishtokenstream.EnglishTokenStream(d.get_content())
        for token in tokens:
            for x in token.split(" "):
                tok = x.strip()
                if (len(tok) > 0):
                    #   Process each token.
                    list_terms = token_processor.process_token(x)
                    if (list_terms is not None):
                        for t in list_terms:
                            #   Add each processed term to the index with .add_term().
                            InvInd.add_term(t, d.id, pos)
                    pos += 1


    
    return InvInd


if __name__ == "__main__":
    corpus_path = Path("json10")
    d = DirectoryCorpus.load_text_directory(corpus_path, ".json")

    # Build the index over this directory.
    index = index_corpus(d)
    
    diw = DiskIndexWriter()
    diw.writeIndex(index, "postings.bin")

    dpi = DiskPositionalIndex("postings.bin")

    choice = 0
    #menu options to loop
    choice = int(input("What would you like to do?\n1) Search a word in documents\n2) Exit\n"))
    # We aren't ready to use a full query parser;
    # for now, we'll only support single-term queries.
    query = ""#"whale" # hard-coded search for "whale"
    while choice != 2:
        idList = []
        chList = []
        #Most of this is uncecessary, I did it for formatting purposes
        query = input("Please enter the word you would like to look for: ")
        b = BooleanQueryParser.parse_query(query)
        if (type(b) is AndQuery or type(b) is OrQuery):
            for p in b.get_postings(dpi):
                print(p)
                idList.append(d.get_document(p.doc_id).title)
        else:
            dpi.get_postings(query)
            for p in dpi.get_postings(str(b)):
                print(p)
                idList.append(d.get_document(p.doc_id).title)
        
        print(len(idList))
        for x in idList:
        #     x = [x.replace("chapter","Chapter ")]
            chList.append(x)
        if idList == []:
            print("Your word was not found in the given documents.")
        else:
            print(f"The word {query} was found in chapters:")
            for y in chList:
                print(y)
        #reloop if wanting to search again
        choice = int(input("Would you like to find another word?\n1) Yes\n2) No\n"))

    # TODO: fix this application so the user is asked for a term to search.
