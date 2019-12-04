import math
import sys
import json
import os
from RunDataTransformer import data_transformation

index_folder_name = "/saved_json_files/"
content_folder_name = "crawled_files/"
num_file_to_process = 1000
top_k = 5

def retrieval_model(index_folder_name, content_folder_name, query, top_k, f):
  '''
  core part of retrieval model, calculating score for each document
  index_folder_name: the name of a folder where you stored the index files
  content_folder_name:the folder containing documents crawled
  query: query from user 
  top_k: the maximum number of results to return for each query
  f: file to write output
   '''
  f.write("Raw query: " + query + "\n")
  query_term = query.split()
  f.write("Tokenized query: " + query + "\n")
  save_path = os.getcwd() + index_folder_name
  with open(save_path + 'term_id_file.json', 'r') as read_file:
   term_id_file = json.load(read_file) # store document frequency for each term
  with open(save_path + 'doc_id_file.json', 'r') as read_file:
   document_id_file = json.load(read_file)
  with open(save_path + 'inverted_index.json', 'r') as read_file:
   inverted_index = json.load(read_file) 
  weighted_term_document = {}
  weighted_term_query = {}
  document_score = {}
  term_tf = get_tf(query_term, inverted_index)
  term_idf = get_idf(query_term, term_id_file)
  
  # calculate tf*idf
  tf_idf = {}
  for term in query_term:
    tf_idf[term] = {}
  for term, doc_idf in term_tf.items():
    for doc, tf in doc_idf.items():
      tf_idf[term][doc] = tf * term_idf[term]

  weighted_term_freq = get_query_term_tf(query_term, term_id_file)

  doc_score = calculate_doc_score(weighted_term_freq, tf_idf, content_folder_name, f)

def calculate_doc_score(weighted_term_freq, weighted_term_doc, content_folder_name, f):
  '''calculate score for each document based on query'''
  score = {}
  rev_weighted_term_doc = {}
  for term, v in weighted_term_doc.items():
    for doc, num in v.items():
      if doc not in rev_weighted_term_doc:
        rev_weighted_term_doc[doc] = {}
      rev_weighted_term_doc[doc][term] = num
  for k in rev_weighted_term_doc.keys():
    sum = 0
    # normalize w_t_d
    for term, num in rev_weighted_term_doc[k].items():
      sum += num ** 2
    for term, num in rev_weighted_term_doc[k].items():
      rev_weighted_term_doc[doc][term] = num / math.sqrt(sum)
  
  doc_content = data_transformation(content_folder_name, num_file_to_process)
  
  
  for doc in rev_weighted_term_doc.keys():
    score[doc] = 0
    for term in weighted_term_freq.keys():
      if term in rev_weighted_term_doc[doc]:
        score[doc] += rev_weighted_term_doc[doc][term] * weighted_term_freq[term]
  ordered = sorted(score.items(), key=lambda x: x[1], reverse=True) # sort the documents by score
  result_list = []
  f.write("DocumentID of the result file: ")
  for k, v in list(ordered)[0:top_k]:
    f.write(k + "\t")
  f.write("\n")

  for k, v in list(ordered)[0:top_k]:
    f.write(k + "(first 200bytes): " + " ".join(doc_content[k][:100]) + "\n\n")

  f.write("Ranked documentID cosine similarity:\n\t")
  for k, v in list(ordered)[0:top_k]:
    result_list.append(k)
    f.write(k + ", score " + "{0:.3f}".format(v) + ";\t")

  f.write("\nTerm contribution to document score:\n\t")
  for doc in rev_weighted_term_doc.keys():
    score[doc] = 0
    for term in weighted_term_freq.keys():
      if term in rev_weighted_term_doc[doc]:
        score[doc] += rev_weighted_term_doc[doc][term] * weighted_term_freq[term]
        if doc in result_list:
          f.write(doc + ": ")
          f.write(term + ": " + "{0:.3f}".format(rev_weighted_term_doc[doc][term] * weighted_term_freq[term]) + ";\t")
  f.write("\n\n\n")
  return result_list
  
  

# <term, idf>
def get_idf(query_term, term_id_file):
  '''Evaluate idf for each document '''
  term_idf = {}
  for term in query_term:
    if term not in term_id_file:
      term_idf[term] = 0
    else:
      freq = term_id_file[term]
      # term_idf[term] = math.log10(num_file_to_process / freq)
      term_idf[term] = 1 # Assume idf = 1
  return term_idf

def get_query_idf(query_term, term_id_file):
  '''Evaluate idf for query '''
  term_idf = {}
  for term in query_term:
    if term not in term_id_file:
      term_idf[term] = 0
    else:
      freq = term_id_file[term]
      term_idf[term] = math.log10(num_file_to_process / freq)
      # term_idf[term] = 1
  return term_idf

# <term, <doc, tf>>
def get_tf(query_term, inverted_index):
  ''' Evaluate tf for each token in the document'''
  term_tf = {}
  for term in query_term:
    term_tf[term] = {}
  for term, doc_term_freq in inverted_index.items():
    if term not in term_tf:
      continue
    for doc_term in doc_term_freq:
      term_tf[term][doc_term[0]] = 1 + math.log10(doc_term[1])
  return term_tf

def get_query_term_tf(query_term, term_id_file):
  '''Evaluate the weighted tf-idf vector for the query'''
  term_idf = get_query_idf(query_term, term_id_file)
  term_frequency = {}
  for term in query_term:
    term_frequency[term] = term_frequency.get(term, 0) + 1
  weighted_term_freq = {}
  for k, v in term_frequency.items():
    weighted_term_freq[k] = (1 + math.log10(v)) * term_idf[k]

  # Normalize the weights
  sum = 0
  for value in weighted_term_freq.values():
    sum += value ** 2
  for k, v in weighted_term_freq.items():
    weighted_term_freq[k] = v / math.sqrt(sum)
  return weighted_term_freq

def main():
  queries = [line.rstrip('\n') for line in open('queries.txt')]
  f = open("output.txt", "w+")
  for query in queries: # run each query to test retrieval model
    retrieval_model(index_folder_name, content_folder_name, query, top_k, f)
  f.close()
  
main()