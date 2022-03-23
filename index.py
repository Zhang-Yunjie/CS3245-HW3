#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import pickle
import os
import math
import string

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    
    # get the list of files inside the input directory
    filenames = []
    for filename in os.listdir(in_dir):
        if not filename.endswith('.DS_Store'):
            filenames.append(filename)
    
    # sort filenames before processing data so docIDs in posting are in order
    filenames.sort()
    
    # Total number of documents
    N = len(filenames)
    
    #print(filenames)
    # Initialize dictionary
    dictionary = {}
    dictionary['DOC_LENGTH'] = {}
   
    # process each file
    for filename in filenames:
        # print(filename)
        full_filename = os.path.join(in_dir, filename)
        text = open(full_filename, 'r', encoding="utf8").read()
                
        """ Process the input text """
        # Apply case folding
        text = text.lower()
                
        # Remove punctuations
        #text = re.sub(r'[^\w\s]', '', text)

        # Initialize term frequency map
        freq_map = {}
        
        # Apply tokenization and stemming
        for sentence in nltk.sent_tokenize(text):
            for word in nltk.word_tokenize(sentence):
                if word in string.punctuation:
                    continue
                stemmed_word = nltk.stem.PorterStemmer().stem(word)
                
                # Update term frequency map
                if stemmed_word not in freq_map:
                    freq_map[stemmed_word] = 1
                else:
                    freq_map[stemmed_word] += 1
       
        doc_length = 0 # initialise document_length for this document 
                       # --> for score normalisation later
        
        # Precompute document frequency and posting list
        for term, tf in freq_map.items():
            # Apply log-frequency weighting scheme
            log_tf = 1 + math.log(tf,10)
            # Update document length
            doc_length += log_tf ** 2
            
            if term not in dictionary:
                dictionary[term] = (1, [(int(filename), log_tf)])
                # structure of each item in the dictionary: 
                # (document_frequency, [(docID_1, log_tf_1), (docID_2, log_tf_2) ... (docID_n, log_tf_n)])
            else:
                # Update current document frequency
                df = dictionary[term][0] + 1
                posting = dictionary[term][1] + [(int(filename), log_tf)]
                dictionary[term] = (df,posting)
        
        # Compute and store the document length for current document, to be used in normalization in searching
        dictionary['DOC_LENGTH'][int(filename)] = math.sqrt(doc_length)
    
    f_dict = open(out_dict, "wb")
    f_post = open(out_postings, 'wb')
    f_dict.truncate(0)
    f_post.truncate(0)
    
    # Write dictionaries and postings to dictionary.txt and posting.txt
    for term, value in dictionary.items():
        if term == "DOC_LENGTH":
            continue
        
        # Store the posting lists
        df,posting = value
        pointer = f_post.tell()
        pickle.dump(posting, f_post)
        
        # Convert df to idf
        idf = math.log((N / df),10)
        
        # Update dictionary with idf and pointer
        dictionary[term] = (idf,pointer)
    
    pickle.dump(dictionary,f_dict)
    f_dict.close()
    f_post.close()
        


input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
