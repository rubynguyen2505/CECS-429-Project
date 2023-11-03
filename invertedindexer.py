#Zach Brown
#025473992
#9/4/23

from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, TermDocumentIndex, PositionalInvertedIndex
from text import BasicTokenProcessor, AdvancedTokenProcessor, englishtokenstream

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
                # print(tok)
                if (len(tok) > 0):
                    list_terms = token_processor.process_token(tok)
                    # print(list_terms)
                    #   Add the processed token (a "term") to the vocabulary set.
                    if (list_terms is not None):
                        for t in list_terms:
                            vocabulary.add(t)


    # TODO:
    # After the above, next:
    # Create a TermDocumentIndex object, with the vocabular you found, and the len() of the corpus.
    InvInd = PositionalInvertedIndex(vocabulary)

    # Iterate through the documents in the corpus:
    for d in corpus:
    #   Tokenize each document's content, again.
        tokens = englishtokenstream.EnglishTokenStream(d.get_content())
        for token in tokens:
            for x in token.split(" "):
                tok = x.strip()
                # print(tok)
                if (len(tok) > 0):
                    list_terms = token_processor.process_token(x)
                    if (list_terms is not None):
                        for t in list_terms:
                            InvInd.add_term(t, d.id)

    #   Process each token.
    #   Add each processed term to the index with .add_term().
    
    return InvInd


if __name__ == "__main__":
    corpus_path = Path("json10")
    d = DirectoryCorpus.load_text_directory(corpus_path, ".json")

    # Build the index over this directory.
    index = index_corpus(d)
    
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
        for p in index.get_postings(query):
            idList.append(d.get_document(p.doc_id).title)
        
        print(len(idList))
        for x in idList:
        #     x = [x.replace("chapter","Chapter ")]
            chList.append(x)
        if idList == []:
            print("Your word was not found in the given documents.")
        else:
            print(f"The word {query} was found in chapters:",*chList)
        #reloop if wanting to search again
        choice = int(input("Would you like to find another word?\n1) Yes\n2) No\n"))

    # TODO: fix this application so the user is asked for a term to search.
