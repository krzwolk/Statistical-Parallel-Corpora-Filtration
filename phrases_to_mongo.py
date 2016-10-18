# Creating MongoDB collection from phrase table

import sys
import os
import codecs
import string
from pymongo import MongoClient

if len(sys.argv) < 3:
	print("Usage: phrases_to_mongo.py filename collection")
	print("Example: phrases_to_mongo.py phrase-table.17 cs_en")
	os._exit(1)
	
# input file
filename = sys.argv[1]	
# collection
coll_name = sys.argv[2]

# Removes punctuation and quotes from given string input_str
def clean_str(input_str):
	str = input_str.replace("&quot;", "")
	return "".join(l for l in str if l not in string.punctuation).strip()

client = MongoClient()
db = client["phrase_table"]

buffer_size = 10000
current_size = 0
line_num = 1
data = []
collection = db[coll_name]

with codecs.open(filename, "r", "utf-8") as sourceFile:
	while True:
		line = sourceFile.readline()
		if not line:
			break
		
		s = line.split("|||")
		s_from, s_to = clean_str(s[0]), clean_str(s[1])
		if not s_from or not s_to:
			continue
			
		line_num += 1
		if (current_size < buffer_size):
			try:
				data.append(
					{ 
						"s_from": s_from, 
						"s_to": s_to
					}
				)
				current_size += 1	
			except:
				print("Unexpected error")
		else:
			print("data count {0} acquired on line {1}".format(len(data), line_num))
			collection.insert_many(data)
			print("inserted")			
			data.clear()
			current_size = 0
			
		
			
collection.insert_many(data)
print("everything is inserted:, {0} lines of input file processed".format(line_num))

print("indexing collection {0}...".format(coll_name))
collection.create_index("s_from")
print("indexing is done, the collection is ready to use")