
from translation_driver import *

# Calculates Levenstein distance for two strings from Entry
def distance(a, b):
	n, m = len(a), len(b)
	
	if n > m:
    	# Make sure n <= m, to use O(min(n,m)) space
		a, b = b, a
		n, m = m, n

	current_row = range(n+1) # Keep current and previous row, not entire matrix
	for i in range(1, m+1):
		previous_row, current_row = current_row, [i]+[0]*n
		for j in range(1,n+1):
			add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
			if a[j-1] != b[i-1]:
				change += 1
			current_row[j] = min(add, delete, change)

	return current_row[n], n, m
	
def split_into_bigrams(str):
	s = str.split(" ")
	ngrams = []
	for i in range(0, len(s) - 1):
		ngrams.append([s[i], s[i + 1]])
	return ngrams
	
def translate_bigrams(driver, bigrams):
	result = []
	for bigram in bigrams:
		bg_str = " ".join(bigram)
		translation = driver.find_translation(bg_str)		
		tr_words = translation.split(" ")
		for word in tr_words:
			result.append(word)
		
	return result
	
def make_bigram_sentence(bigrams):
	result = []
	for bigram in bigrams:
		for word in bigram:
			result.append(word)
		
	result.sort()
	return result
	
def levenstein_filtering(entry):

	src_ngrams = split_into_bigrams(entry.src_string)
	res_ngrams = split_into_bigrams(entry.res_string)
	
	upper_bound = distance(" ".join(make_bigram_sentence(src_ngrams)), " ".join(make_bigram_sentence(res_ngrams)))
	if upper_bound[0] == 0:
		return 0
	
	src_tr = translate_bigrams(TranslationDriver(entry.src_lang), src_ngrams) #entry.src_lang)
	res_tr = translate_bigrams(TranslationDriver(entry.res_lang), res_ngrams) #entry.res_lang)
	
	src_tr.sort()
	res_tr.sort()
	real_distance = distance(" ".join(src_tr), " ".join(res_tr))	

	return 100.0 - (real_distance[0] * 100.0 / upper_bound[0])