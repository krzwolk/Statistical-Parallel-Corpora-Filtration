# Translation filtering

from pymongo import MongoClient

class TranslationDriver:
	def __init__(self, lang_from):
		self.trivial = False
		if lang_from == "en":
			self.trivial = True
		
		if not self.trivial:
			client = MongoClient()
			db = client["phrase_table"]
			self.collection = db[lang_from + "_en"]

	def find_translation(self, start_with):
		if self.trivial:
			return start_with
			
		#res = self.collection.find({'s_from':{'$regex':'^{0}'.format(start_with)}})
		res = self.collection.find({'s_from':start_with})
		try:
			return res[0]["s_to"]
		except:
			# no results found
			return start_with