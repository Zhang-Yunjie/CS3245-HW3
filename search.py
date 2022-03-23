#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import heapq
import pickle
import math

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # This is an empty method
    # Pls implement your code in below
    
    file = open(dict_file, 'rb')
    # load dictionary file into memory
    dictionary = pickle.load(file)
    file.close()
    
    postings_file = open(postings_file, 'rb')
    
    # Obtain input and output files, parse the queries into list
    in_file = open(queries_file, 'r', encoding="utf8")
    out_file = open(results_file, 'w', encoding="utf8")
    out_file.truncate(0) # clear output file
    content = in_file.read()
    query_list = content.splitlines() # remove the "\n" mark at the end of each line
    
    while query_list:
        query = query_list.pop(0) # get current query
        if not query:
            out_file.write("")
        else:
            result = rank(query,dictionary,postings_file)
            final_result = " ".join(result)
            out_file.write(final_result)
            
        # if current line is not the last line, add a line break
        if query_list:
            out_file.write('\n')
            
            
            
def rank(query,dictionary,postings_file):
    query_term_vector = computeQueryVector(query,dictionary,postings_file)
    term_doc_dictionary = {}
    candidates = set() # store unique docIDs that have one of the term in the query
    
    for term in query_term_vector.keys():
        score = 0
        term_doc_dictionary[term] = {}
        
        if term in dictionary:
            value = dictionary[term]
            pointer = value[1]
            postings_file.seek(pointer)
            posting = pickle.load(postings_file)
            
            for docID,log_tf in posting:
                document_length = dictionary["DOC_LENGTH"][docID]
                # Apply length normalization
                term_doc_dictionary[term][docID] = log_tf / document_length
                candidates.add(docID)
    
    # sort candidates
    #candidates = sorted(list(candidates))
    
    pq = []
    
    for docID in candidates:
        score = 0
        
        for term in query_term_vector.keys():
            if docID not in term_doc_dictionary[term]:
                continue
            else:
                # compute cosine similarity using dot product
                term_query_score = query_term_vector[term]
                term_doc_score = term_doc_dictionary[term][docID]
                cos_similarity = term_query_score * term_doc_score
                score += cos_similarity
        
        # Sort by decreasing order of the score, but sort ascending of doc id if the score is the same
        heapq.heappush(pq, (score, -1 * int(docID)))
    
    return map(lambda x: str(-1 * x[1]),heapq.nlargest(10, pq))
        

def computeQueryVector(query,dictionary,postings_file):
    # Tokenize query, apply stemming and case folding, split query by " "
    stemmer = nltk.stem.PorterStemmer()
    token_list = list(map(lambda x: stemmer.stem(x).lower(), query.split(" ")))
    filtered_list = [token for token in token_list if token not in string.punctuation] # remove tokens that are solely punctuations
    
    # Count frequency for each token in query
    term_freq = {}
    for token in token_list:
        if token not in term_freq:
            term_freq[token] = 1
        else:
            term_freq[token] += 1
    
    #query_length = 0
    query_term_vector = {}
    
    # Compute tf-idf for query
    for term in term_freq.keys():
        score = 0
        if term in dictionary:
            value = dictionary[term]
            idf = value[0]
            tf = term_freq[term]
            log_tf = 1 + math.log(tf,10)
            score = log_tf * idf
        
        query_term_vector[term] = score

    return query_term_vector
    
    
dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
