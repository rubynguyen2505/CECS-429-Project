from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, TermDocumentIndex
from text import BasicTokenProcessor, englishtokenstream
"""This basic program builds a term-document matrix over the .txt files in
the same directory as this file."""
def index_corpus(corpus : DocumentCorpus) -> Index:
    token_processor = BasicTokenProcessor()
    vocabulary = set()

    for d in corpus:
        print(f"Found document {d.title}")
        # Tokenize the document's content by creating an EnglishTokenStream around the document's .content()
        tokenizer = englishtokenstream.EnglishTokenStream(d.get_content())
        # Iterate through the token stream, processing each with token_processor's process_token method.
        # # Add the processed token (a "term") to the vocabulary set.
        for token in tokenizer:
            t = token_processor.process_token(token)
            vocabulary.add(t)

    # After the above, next:
    # Create a TermDocumentIndex object, with the vocabular you found, and the len() of the corpus.
    termDocIndex = TermDocumentIndex(vocabulary, len(corpus))
    # Iterate through the documents in the corpus:
    docID = 0
    for d in corpus:
        # Tokenize each document's content, again.
        tokenizer = englishtokenstream.EnglishTokenStream(d.get_content())
        # Process each token.
        # Add each processed term to the index with .add_term().
        for token in tokenizer:
            t = token_processor.process_token(token)
            termDocIndex.add_term(t, docID)
        docID += 1

    return termDocIndex

"""
if __name__ == "__main__":
    corpus_path = Path()
    d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")
    # Build the index over this directory.
    index = index_corpus(d)
    # We aren't ready to use a full query parser;
    # for now, we'll only support single-term queries.
    userQuery = input("Please enter a query (type quit to end the query process):")
    while (userQuery != "quit"):
        for p in index.get_postings(userQuery):
            print(f"Document ID {p.doc_id}")
        userQuery = input("Please enter a query (type quit to end the query process): ")
    print("The query process has ended!")
"""