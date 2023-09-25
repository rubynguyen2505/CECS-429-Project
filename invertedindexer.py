from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, InvertedIndex, PositionalInvertedIndex
from text import BasicTokenProcessor, englishtokenstream

"""This basic program builds a term-document matrix over the .txt files in 
the same directory as this file."""

def index_corpus(corpus : DocumentCorpus) -> Index:
    
    token_processor = BasicTokenProcessor()
    vocabulary = set()
    
    for d in corpus:
        
        print(f"Found document {d.title}")
        #   Tokenize the document's content by creating an EnglishTokenStream around the document's .content()
        #   tokenizer = englishtokenstream.EnglishTokenStream(d.get_content())
        #   Iterate through the token stream, processing each with token_processor's process_token method.
        #   Add the processed token (a "term") to the vocabulary set.
        """
        for token in tokenizer:
            t = token_processor.process_token(token)
            vocabulary.add(t)
        """
    """    
    # After the above, next:
    # Create a InvertedIndex object.
    invertedIndex = InvertedIndex(vocabulary)
    # Iterate through the documents in the corpus:
    docID = 0
    for d in corpus:
        #   Tokenize each document's content, again.
        tokenizer = englishtokenstream.EnglishTokenStream(d.get_content())
        #   Process each token.
        #   Add each processed term to the index with .add_term().
        for token in tokenizer:
            t = token_processor.process_token(token)
            invertedIndex.addTerm(t, docID)
        docID += 1
    """
    return None



if __name__ == "__main__":
    
    corpus_path = Path(r"D:\all-nps-sites-extracted")
    d = DirectoryCorpus.load_text_directory(corpus_path, ".json")

    # Build the index over this directory.
    index = index_corpus(d)

    userQuery = input("Please enter a query (type quit to end the query process): ")
    while (userQuery != "quit"):
        print(f"Found term '{userQuery}' in the following documents:")
        for p in index.getPostings(userQuery):
            print(d.get_document(p.doc_id).title)
        userQuery = input("Please enter a query (type quit to end the query process): ")
    print("The query process has ended!")
