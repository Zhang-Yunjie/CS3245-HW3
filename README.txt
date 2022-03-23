This is the README file for A0204848Y-A0204208U's submission
Email(s): e0421414@u.nus.edu, e0424771@u.nus.edu

== Python Version ==

We're using Python Version 3.7.6 for
this assignment.

== General Notes about this assignment ==


1. Index Construction
    1.1 We removed stand alone punctuations. (e.g. "." in 1.2 is not removed, but "-" a - b is removed)
    1.2 Each entry in the dictionary contains the idf of the term and the pointer to the postings list of the term.
    1.3 We also stored the doc_length of all documents in the dictionary, for normalization later
    1.4 Each postings list contains pairs of (docID, log_tf) 
2. Length Normalization
    We chose to only normalize documents. 
    We chose to apply normalization when processing queries because it requires only one division 
    on the final score of a document instead of one division on every dimension
3. Search
    3.1 We calculated the score of each term in the query based on the cosine of the angle between the query vector and document vector
    3.2 Query vector calculation is similar to that of document vector calculation, but we did not normalize
    query vectors because the length of query vector is the same when we compare across documents. Not normalizing
    does not affect the ranking.
    3.3 We then choose 10 documents with the highest score



== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

README.txt
index.py 
search.py
postings.txt
dictionary.txt

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] We, A0204848Y and A0204208U, certify that we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, we
expressly vow that we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>
