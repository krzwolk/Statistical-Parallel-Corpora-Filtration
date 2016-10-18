

class Entry:
	def __init__(self, src_lang, res_lang, src_string, res_string):
		self.src_lang = src_lang
		self.res_lang = res_lang
		self.src_string = src_string		
		self.res_string = res_string	
		
	def __str__(self):
		return "{0}: {1}\n{2}: {3}".format(self.src_lang, 
			self.src_string, 
			self.res_lang, 
			self.res_string)