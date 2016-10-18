import sys
import os
import os.path
import codecs

from rule_filtering import *
from levenstein_filtering import *

from entry import Entry
from tmx_reader import TMXReader
from tmx_writer import TMXWriter
from txt_reader import TXTReader
from txt_writer import TXTWriter

def get_filename(path):
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)

if len(sys.argv) < 4:
	print("Usage: main.py file1 file2 outdir")
	print("Example: main.py Wikipedia.cs-en.cs Wikipedia.cs-en.en ./output")
	os._exit(1)

file1 = sys.argv[1]
file2 = sys.argv[2]
outdir = sys.argv[3]

rdr = TXTReader(file1, file2)
good = TXTWriter(os.path.join(outdir, "good_" + get_filename(file1)), os.path.join(outdir, "good_" + get_filename(file2)))
bad = TXTWriter(os.path.join(outdir, "bad_" + get_filename(file1)), os.path.join(outdir, "bad_" + get_filename(file2)))

# threshold for number filtering points, so, first parameter num_p_threshold is involved in rule-based filtering. The first rule is checking numbers inside sentence. If num_p_threshold = 65, that means that 65% of numbers in two strings should match. For example, if first sentence contains numbers 1, 2, and 3, and second one contains 1, 2 and 4, then 66% of numbers match, so such sentence pair passes this rule
num_p_threshold = 65.0

short_len_min = 12 # minimal string length, short_len_min = 12 means that both sentences must be not shorter than 12 character - this allows to filter garbage sentences with ISBNs and other unrelated stuff
shortlen_p_threshold = 100.0 # only two values are possible: 0 and 100, max_word_count = 100 means that both sentences must not be longer than 100 words. This rule is needed to filter very large sentences (we saw such large blocks of text which dramatically reduce performance of levenstein filter)

lev_threshold = 5 # minimal levenstein points

def result(ok):
	if ok:
		return "good"
	else:
		return "bad"		
		
for entry_num, entry in enumerate(rdr):
	num_p = number_filtering(entry)
	shortlen_p = short_length_filtering(entry, short_len_min)

	ok = num_p >= num_p_threshold and shortlen_p >= shortlen_p_threshold
	if ok:
		lev_p = levenstein_filtering(entry)
		ok = ok and lev_p >= lev_threshold
		if ok:
			good.write(entry)
			print("{0} good, levenstein distance points {1}".format(entry_num, lev_p))
		else:
			bad.write(entry)
			print("{0} bad, levenstein distance points {1}".format(entry_num, lev_p))
	else:
		bad.write(entry)
		print("{0} bad, rule filtering".format(entry_num))
		
good.save()
bad.save()

print("good {0}".format(good.get_entries()))
print("bad {0}".format(bad.get_entries()))
