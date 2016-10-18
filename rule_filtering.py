# Filtering rules
import re

# Finds numbers in entry and checks if the numbers are in both strings
# Returns points from 0 to 100
def number_filtering(entry):
	src_nums = re.findall("\d+", entry.src_string)
	res_nums = re.findall("\d+", entry.res_string)
	distinct_nums = set(src_nums + res_nums)

	if len(distinct_nums) == 0:
		# if there are no numbers in strings - return 100 points
		return 100
		
	step = 100.0 / len(distinct_nums)
	summ = 0
	for n in distinct_nums:
		if n in src_nums and n in res_nums:
			summ += step
			
	return summ
	
# Filters out strings that are shorter that min_len
def short_length_filtering(entry, min_len):
	if len(entry.src_string) < min_len or len(entry.res_string) < min_len:
		return 0
	else:
		return 100

		