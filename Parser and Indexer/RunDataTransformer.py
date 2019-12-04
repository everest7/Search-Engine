import os
import re
import urllib
import string
import json
import sys

folder_name = "crawled_files"


# part1
def data_transformation(folder_name, num_files_to_process, stat):
    ''' tokenize the documents crawled in assignment1 '''
    file_list = os.listdir(folder_name)
    if '.DS_Store' in file_list:
        file_list.remove('.DS_Store')
    file_list = file_list[:num_files_to_process]
    res = {}
    input_files_size = 0
    for file_name in file_list:
        res[file_name] = []
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'crawled_files/')
        # using regex to deal with markup and split the rest into a series of tokens
        with open(final_directory+file_name) as f:
            stat_info = os.stat(final_directory+file_name)
            input_files_size += stat_info.st_size
            raw_data = f.read()
            raw_data = re.sub(
                r"(?is)<script[^>]*>(.*?)</script>", r'', raw_data)
            raw_data = re.sub(
                r"(?is)<style[^>]*>(.*?)</style>", r'', raw_data)
            raw_data = re.sub(
                r"(?is)<annotation[^>]*>(.*?)</annotation>", r'', raw_data)
            raw_data = re.sub(r"(?is)<mo[^>]*>(.*?)</mo>", r'', raw_data)
            raw_data = re.sub(r"(?is)<mi[^>]*>(.*?)</mi>", r'', raw_data)
            raw_data = re.sub(r"(?is)<!--[^>]*>(.*?)-->", r'', raw_data)
            raw_data = re.sub(
                r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});", r'', raw_data)
            raw_data = re.sub(r"<.*?>", r'', raw_data)
            raw_data = re.sub(r'(?<!\w)([A-Z])\.', r'\1', raw_data)
            raw_data = re.sub(r'[^\x00-\x7F]+', r'', raw_data)
            raw_data = re.sub(r'(?<=\d)[,\.](?=\d)', r'', raw_data)
            raw_data = raw_data.replace(".Net", "")
            raw_data = raw_data.replace("2Pac", "")
            for ch in string.punctuation:
                raw_data = raw_data.replace(ch, " ") 
            res[file_name] = raw_data.split()
    stat[0] = input_files_size
    return res


