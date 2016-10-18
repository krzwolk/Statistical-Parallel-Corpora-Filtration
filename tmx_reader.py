# TMX (Translation Memory eXchange) files reader 

import xml.etree.ElementTree as ET
from entry import Entry

class TMXReader:
	namespaces = {'xml': '{http://www.w3.org/XML/1998/namespace}'} 
	lang_key = namespaces["xml"] + "lang"
	
	def __init__(self, filename):
		self.filename = filename
		self.root = ET.parse(filename).getroot()
		self.src_lang = self.root.find("header").get("srclang")
		self.body = self.root.find("body")
	
	def __iter__(self):		
		self.current = 0
		return self
		
	def __next__(self): 
		if self.current >= len(self.body):
			raise StopIteration
		else:
			self.current += 1
			return self.make_entry(self.body[self.current - 1])
			
	def __getitem__(self, key):
		return self.make_entry(self.body[key])
	
	def make_entry(self, xml_entry):
		tuvs = xml_entry.findall("tuv")
		src_tuv = self.find_src_node(tuvs)
		res_tuv = self.find_res_node(tuvs)
				
		src_lang = src_tuv.get(TMXReader.lang_key)
		res_lang = res_tuv.get(TMXReader.lang_key)
		src_string = src_tuv.find("seg").text
		res_string = res_tuv.find("seg").text
		return Entry(src_lang, res_lang, src_string, res_string)
		
	def find_src_node(self, nodes):
		for n in nodes:
			lang_key = TMXReader.namespaces["xml"] + "lang"
			if n.get(lang_key) == self.src_lang:
				return n
	
	def find_res_node(self, nodes):
		for n in nodes:
			lang_key = TMXReader.lang_key
			if n.get(lang_key) != self.src_lang:
				return n
