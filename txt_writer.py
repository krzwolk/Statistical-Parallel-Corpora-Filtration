
import codecs

class TXTWriter:
	namespaces = {'xml': '{http://www.w3.org/XML/1998/namespace}'} 
	lang_key = namespaces["xml"] + "lang"

	def __init__(self, file1, file2):
		self.file1 = codecs.open(file1, "w", "utf-8") #open(file1, "w")
		self.file2 = codecs.open(file2, "w", "utf-8") #open(file2, "w")
		self.entries = 0
		
	def write(self, entry):
		self.file1.write(entry.src_string)
		self.file2.write(entry.res_string)
		self.entries += 1
		
	def save(self):
		self.file1.close()
		self.file2.close()
		
	def get_entries(self):
		return self.entries