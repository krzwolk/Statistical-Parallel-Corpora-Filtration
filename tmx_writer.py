# TMX (Translation Memory eXchange) files writer 

import xml.etree.ElementTree as ET
import datetime 
from entry import Entry

class TMXWriter:
	namespaces = {'xml': '{http://www.w3.org/XML/1998/namespace}'} 
	lang_key = namespaces["xml"] + "lang"

	def __init__(self, filename):
		self.filename = filename
		self.root = ET.Element("tmx", version="1.4")
		self.header = None
		self.body = None
		self.entries = 0
		
	def write(self, entry):
		if self.header is None:
			# creating a header
			self.header = ET.SubElement(self.root, "header", 
										creationdate = str(datetime.datetime.now()),
										srclang = entry.src_lang,
										adminlang = entry.src_lang,
										segtype = "sentence",
										creationtool = "Uplug",
										creationtoolversion = "unknown",
										datatype="PlainText")
			self.header.set("o-tmf", "unknown")
			self.body = ET.SubElement(self.root, "body")


		# writing an entry
		tu  = ET.SubElement(self.body, "tu")
		# source tuv element
		tuv_src = ET.SubElement(tu, "tuv")
		tuv_src.set(TMXWriter.lang_key, entry.src_lang)
		seg_src = ET.SubElement(tuv_src, "seg")
		seg_src.text = entry.src_string
		# results tuv element
		tuv_res = ET.SubElement(tu, "tuv")
		tuv_res.set(TMXWriter.lang_key, entry.res_lang)
		seg_res = ET.SubElement(tuv_res, "seg")
		seg_res.text = entry.res_string
		
		self.entries += 1
	
	def save(self):
		tree = ET.ElementTree(self.root)
		tree.write(self.filename, encoding='utf-8', xml_declaration=True)
		
	def get_entries(self):
		return self.entries