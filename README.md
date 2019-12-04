# How does a Search Engine work?

Search engines usually have three components.


![alt text](https://upload.wikimedia.org/wikiversity/en/thumb/f/fb/High_level_architecture_of_a_Search_Engine.png/256px-High_level_architecture_of_a_Search_Engine.png "Search Engine Component")



**Crawler**: Givent a seedURL, scour the internet, extract the links from each page, and keep track of the pages you have crawled. In crawling, we observe the politeness rules and wait at least one second between requests to the web server to get new pages.


**Parser and Indexer**: Transform crawled documents and make them ready to be indexed. Tokenize the documents crawled previously. In this step, we need to deal with markup like HTML tags and split the rest of each file into a series of tokens. The index are created as following:

1. A file TermIDFile that contains data structure(s) that map terms into TermIDs and stores document frequencies with the TermIDs. The document frequency for a term is the number of files that the term occurs in.

2. A file DocumentIDFile that contains data structure(s) that map DocumentIDs to document names and stores the document length with each DocumentID. For document length, store the number of the tokens in the document. (For document length, you could alternatively store the document file length in bytes, but total number of tokens is better).

3. A file named InvertedIndex that stores a collection of inverted lists, one for each TermID. Each inverted list is a list of postings, where each posting contains a DocumentID and the relevant term frequency. This will be the biggest of the 3 files.


**retrieval & ranking system**: Rank all documents in the index for each query using cosine similarity and vector space ranking, and write out the top K results.
1. Run the same tokenization and data transformation on each query.
2. Keep track of the transformed query tokens.
3. Represent each transformed query as a normalized, weighted tf-idf vector (lnc.ltc weighting)
4. Represent each document similarly as a normalized, weighted tf-idf vector (lnc.ltc weighting)
5. For each query,
  a. Compute the cosine similarity score for the query vector and each document vector.
  b. Rank (sort) the documents with respect to the query by the cosine similarity score.
  c. Return the top K documents as results, in descending order of the cosine score.