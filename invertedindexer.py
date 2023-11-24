#Zach Brown
#025473992
#9/4/23

from pathlib import Path
from queue import PriorityQueue
import math
import struct
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, TermDocumentIndex, PositionalInvertedIndex, DiskIndexWriter, DiskPositionalIndex
from text import BasicTokenProcessor, AdvancedTokenProcessor, englishtokenstream
from querying import BooleanQueryParser, AndQuery, OrQuery

"""This basic program builds a term-document matrix over the .txt files in 
the same directory as this file."""

doc_length_d = {}
doc_length_A = 0
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

    with open('docWeights.bin', 'wb') as file:

        # Iterate through the documents in the corpus:
        for d in corpus:
            l_d = 0
            sum_square_tftd = 0
            tftd = {}
            pos = 0
            #   Tokenize each document's content, again.
            tokens = englishtokenstream.EnglishTokenStream(d.get_content())
            for token in tokens:
                for x in token.split(" "):
                    tok = x.strip()
                    if (len(tok) > 0):
                        #   Process each token.
                        f = doc_length_d.get(d.id)

                        if f == None:
                            doc_length_d[d.id] = 1
                        else:
                            doc_length_d[d.id] += 1
                        
                        list_terms = token_processor.process_token(tok)
                        if (list_terms is not None):
                            for t in list_terms:
                                #   Add each processed term to the index with .add_term().
                                InvInd.add_term(t, d.id, pos)
                                frequency = tftd.get(t)

                                if frequency == None:
                                    tftd[t] = 1
                                else:
                                    tftd[t] += 1
                        pos += 1
            for term in tftd:
                sum_square_tftd += math.pow(tftd.get(term), 2)
            l_d = (int)(math.sqrt(sum_square_tftd))
            file.write(struct.pack("i", l_d))
        file.close()


    
    return InvInd

def okapi_25(corpus_size : int, index : DiskPositionalIndex, query : str):
    query_terms = query.split()
    A_d = {}
    doc_length_sum = 0
    for d in doc_length_d:
        doc_length_sum += doc_length_d.get(d)
    doc_length_A = doc_length_sum / len(doc_length_d)
    for term in query_terms:
        p_list = index.get_postings(term)
        wqt = max(0.1, math.log((corpus_size - len(p_list) + 0.5) / (len(p_list) + 0.5), math.e))
        for d in p_list:
            wdt = (2.2 * len(d.position)) / (1.2 * (0.25 + 0.75 * (doc_length_d.get(d.doc_id) / doc_length_A)) + len(d.position))
            accumulator = A_d.get(d.doc_id)
            if accumulator == None:
                A_d[d.doc_id] = 0
            A_d[d.doc_id] += wqt * wdt
    
    q = PriorityQueue()

    
    for d in A_d:
        quotient = A_d.get(d)/1
        q.put((quotient * (-1), d))
    
    top_10 = []
    i = 0
    while i < 5:
        next_item = q.get()
        print(next_item)
        top_10.append(list(next_item))
        top_10[i][0] = top_10[i][0]/(-1)
        i += 1
    return top_10

def ranked_retrieve(corpus_size : int, index : DiskPositionalIndex, query : str):
    query_terms = query.split()
    A_d = {}
    for term in query_terms:
        p_list = index.get_postings(term)
        wqt = math.log((1 + corpus_size/len(p_list)), math.e)
        for d in p_list:
            wdt = 1 + math.log(len(d.position), math.e)
            accumulator = A_d.get(d.doc_id)
            if accumulator == None:
                A_d[d.doc_id] = 0
            A_d[d.doc_id] += wqt * wdt
    
    q = PriorityQueue()

    with open('docWeights.bin', 'rb') as file:
        for d in A_d:
            l_d = list(struct.unpack("i", file.read(4)))
            quotient = A_d.get(d)/l_d[0]
            q.put((quotient * (-1), d))
        file.close()
    
    top_10 = []
    i = 0
    while i < 5:
        next_item = q.get()
        print(next_item)
        top_10.append(list(next_item))
        top_10[i][0] = top_10[i][0]/(-1)
        i += 1
    return top_10

        





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
        choice_ranking = 0
        choice_ranking = int(input("How would you like to rank your query?\n1) By default\n2) Okapi 25\n3) Return\n"))
        while choice_ranking != 3:
            if choice_ranking == 1:
                top_10 = ranked_retrieve(len(d), dpi, query)
                for item in top_10:
                    print(d.get_document(item[1]), ": score -", item[0])
            else:
                top_10 = okapi_25(len(d), dpi, query)
                for item in top_10:
                    print(d.get_document(item[1]), ": score -", item[0])
            choice_ranking = int(input("Would you like to rank again?\n1) By default\n2) Okapi 25\n3) No\n"))

        choice = int(input("Would you like to find another word?\n1) Yes\n2) No\n"))

    # TODO: fix this application so the user is asked for a term to search.
