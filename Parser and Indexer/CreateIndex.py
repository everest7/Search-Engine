from RunDataTransformer import data_transformation

import os
import json

# input parameter
folder_name = "crawled_files"
num_files_to_process = 1000
# global variables
stat = [0, 0, 0, 0, 0] # storing statistics information
stat_file = "stats.txt"
file_mode = 'w+'

# part2
def indexing(input):
    ''' Create inverted index with the tokens from part1'''
    term_id_file = {} # map terms into document frequencies with the termID
    document_id_file = {} # map document ID to document name and the document length
    inverted_index = {} # map term to a list of postings(document ID and term frequency)
    word_to_file = {} # map term to document
    for doc_id, words in input.items():
        document_id_file[doc_id] = (doc_id, len(words))
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
            if word not in word_to_file:
                word_to_file[word] = set()
            word_to_file[word].add(doc_id)
        for word, count in word_count.items():
            if word not in inverted_index:
                inverted_index[word] = []
            inverted_index[word].append((doc_id, word_count[word]))
    for word, files in word_to_file.items():
        term_id_file[word] = len(files)

    # store stat infomation
    total_terms = 0
    for key, value in inverted_index.items():
        terms_freq = [x[1] for x in value]
        total_terms += sum(terms_freq)
    stat[1] = total_terms # Total number of tokens across all input files
    stat[2] = len(term_id_file) # Total number of unique tokens across all input files
    current_directory = os.getcwd()
    
    # save stored data as json file
    save_path = os.getcwd() + "/saved_json_files/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(save_path + "term_id_file.json", "w") as termID_file:
        json.dump(term_id_file, termID_file)
        stat_info = os.stat(save_path + "term_id_file.json")
        stat[3] += stat_info.st_size
    termID_file.close()
    with open(save_path + "doc_id_file.json", "w") as docID_file:
        json.dump(document_id_file, docID_file)
        stat_info = os.stat(save_path + "doc_id_file.json")
        stat[3] += stat_info.st_size
    docID_file.close()
    with open(save_path + "inverted_index.json", "w") as inverted_index_file:
        json.dump(inverted_index, inverted_index_file)
        stat_info = os.stat(save_path + "inverted_index.json")
        stat[3] += stat_info.st_size # Total index size, that is total size of the three index files
    inverted_index_file.close()
    stat[4] = 0 if stat[0] == 0 else stat[3] / stat[0] # ratio of the total index size to the total file size
    f = open(stat_file, file_mode) 
    f.write("Total file size of all the input files: " + str(stat[0]) + " bytes\n")
    f.write("Total number of tokens across all input files: " + str(stat[1]) + "\n")
    f.write("Total number of unique tokens across all input files: " + str(stat[2]) + "\n")
    f.write("Total index size, that is total size of the three index files: " + str(stat[3]) + " bytes\n")
    f.write("Ratio of the total index size to the total file size: {:.3f}".format(stat[4]) + "\n")
    f.close()

def main():
  processed_data = data_transformation(folder_name, num_files_to_process, stat)
  indexing(processed_data)

main()


