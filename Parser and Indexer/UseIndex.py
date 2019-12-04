import sys
import json
import os

json_file_folder = "/saved_json_files/"
save_path = os.getcwd() + json_file_folder

def user_query():
  with open(save_path + 'inverted_index.json', 'r') as read_file:
   inverted_index = json.load(read_file)
  query = input('Please enter a query: ')
  print('Query you\'re looking for: ', query)
  print('Documents that contain the query are listed:')
  if query not in inverted_index:
    print("Term cannot be found")
    return
  document_list = [x[0] for x in inverted_index.get(query)]
  
  print(document_list)

user_query()