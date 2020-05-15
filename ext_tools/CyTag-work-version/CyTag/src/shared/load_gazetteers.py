import sys
import os

def load_gazetteers():
	# Create a dictionary to hold the gazetteers
	gazetteers = {}
	# For every file in the cy_gazetteers folder:
	for gaz in os.listdir("{}/../../cy_gazetteers".format(os.path.dirname(os.path.abspath(__file__)))):
		if gaz.rpartition(".")[-1] not in ["py", "json"]: 
			with open("{}/../../cy_gazetteers/{}".format(os.path.dirname(os.path.abspath(__file__)), gaz), encoding="utf-8") as loaded_gazetteer:
				# Set up an 'exclude string' variable, which will contain regex negative lookbehind assertions for each term in the gazetteers
				exclude_string = ""
				# Split the loaded gazetteer into a list of terms
				terms = loaded_gazetteer.read().splitlines()
				for term in terms:
					# For each term, replace full stops with full stops enclosed by square brackets, then create a regex negative lookbehind assertion for the term and add it to the exclude string 
					term = term.replace(".", "[.]")
					exclude_string = exclude_string + "(?<!" + term + ")"
				# Split the name of the gazetteer file into two, and add two new entries to the gazetteer dictionary using the extension (i.e. abbreviations, acronyms) - EXTENSION (consisting of the regular terms) and EXTENSION_regex (consisting of the regex-formatted negative lookbehind assertions for each term)
				gaz_name, gaz_ext = os.path.splitext(gaz)
				gazetteers[gaz_ext[1:]] = terms
				gazetteers["{}_regex".format(gaz_ext[1:])] = exclude_string
	# Return the gazetteers dictionary
	return(gazetteers)