import sys
import os

def load_lexicon():
	# Create a dictionary to hold the lexicon
	lexicon = {}
	with open("{}/../../lexicon/{}".format(os.path.dirname(os.path.abspath(__file__)), "corcencc_lexicon_2017-09-29"), encoding="utf-8") as loaded_lexicon:
		# Open the pre-existing (CorCenCC-formatted) lexicon and create entries by splitting its lines 
		entries = loaded_lexicon.read().splitlines()
		# For each entry loaded from the lexicon...
		for entry in entries:
			if entry[:1] != "#":
				# Split the parts of the entry by tab
				entry_parts = entry.split("\t")
				# If a word is not already in the lexicon dictionary, format the appropriate information and add it to a new list for that word in the lexicon
				if entry_parts[0] not in lexicon.keys():
					lexicon[entry_parts[0]] = [{"lemma": entry_parts[1], "lemma_en": entry_parts[2], "pos_basic": entry_parts[3], "pos_enriched": entry_parts[4]}]
				# Otherwise (if a word is already in the lexicon dictionary), format the appropriate information and append it to the existing list for that word in the lexicon
				else:
					lexicon[entry_parts[0]].append({"lemma": entry_parts[1], "lemma_en": entry_parts[2], "pos_basic": entry_parts[3], "pos_enriched": entry_parts[4]})
	# Return the lexicon dictionary
	return(lexicon)					