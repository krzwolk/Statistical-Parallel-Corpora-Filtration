
import linecache
from entry import Entry

class TXTReader:
	def __init__(self, file1, file2):
		self.file1 = file1
		self.file2 = file2
		
		s = file1.split(".")
		self.src_lang = s[len(s) - 1]
		s = file2.split(".")
		self.res_lang = s[len(s) - 1]
		
	def __iter__(self):		
		self.current = 0
		return self
		
	def __next__(self): 
		self.current += 1
		return self.make_entry(self.current - 1)

			
	def __getitem__(self, key):
		return self.make_entry(key)
		
	def make_entry(self, line_num):
		src_string = linecache.getline(self.file1, line_num + 1)
		res_string = linecache.getline(self.file2, line_num + 1)

		if src_string == "" or res_string == "":
			print(src_string)
			print(res_string)
			raise StopIteration
		return Entry(self.src_lang, self.res_lang, src_string, res_string)