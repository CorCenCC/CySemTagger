#!usr/bin/env python3
#-*- coding: utf-8 -*-
"""
'evaluate_cytag.py'

Compare XML-formatted CyTag output against a given gold standard (CyTag XML-formatted) dataset.

Accepts as arguments:
	--- OPTIONAL: 'soft' (for a more lenient evaluation of CyTag output).
	--- REQUIRED: A gold standard (CyTag XML-formatted) dataset.
	--- REQUIRED: XML-formatted CyTag output to be evaluated.

Developed at Cardiff University as part of the CorCenCC project (www.corcencc.org).

2016-2017 Steve Neale <steveneale3000@gmail.com, NealeS2@cardiff.ac.uk>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses>.
"""

import sys
import os

try:
	import numpy as np
except ImportError:
	pass
try:
	from lxml import etree
except ImportError:
	pass

from shared.check_libraries import *

def evaluate(leniency, gold_file, tagged_file):
	# Check for the python libraries required by evaluate_cytag
	library_info = check_libraries("evaluate_cytag", "evaluate_cytag - Compare CyTag output against a gold standard dataset", ["numpy", "lxml"])
	# If anything other than 'None' was returned from the library check, print it and then return
	if library_info != None:
		print(library_info)
		return
	# Otherwise...
	else:
		print("\nevaluate_cytag - Compare CyTag output against a gold standard dataset\n---------------------------------------------------------------------\n")
		# Set up an XML parser
		parser = etree.XMLParser(remove_blank_text=True)
		# Parse the gold and tagged files as separate lxml trees
		gold_tree = etree.parse(gold_file, parser)
		tagged_tree = etree.parse(tagged_file, parser)
		# Find the tokens in the gold and tagged lxml trees
		gold_tokens = gold_tree.xpath("file/paragraph/sentence/token[@id]")
		all_tagged_tokens = tagged_tree.xpath("file/paragraph/sentence/token[@id]")
		# Find the token IDs of the gold tree tokens
		gold_token_ids = [int(token.attrib["id"]) for token in gold_tokens]
		# Find only those tagged tokens that are also present in the list of gold tokens
		tagged_tokens = [token for token in all_tagged_tokens if int(token.attrib["id"]) in gold_token_ids]
		# Create a variable to store the number of unknown tokens
		unknown = 0
		# Create variables to store the numbers of basic and rich POS tagging errors
		basic_errors, rich_errors = 0, 0
		# For each token in the tagged tree...
		for token_id, tagged_token in enumerate(tagged_tokens):
			# Find the corresponding gold standard token
			gold_token = gold_tokens[token_id]
			# If the basic POS tag for the tagged token is 'unk', increment the number of unknown tokens by one
			if tagged_token.attrib["basic_pos"] == "unk":
				unknown += 1
			# Otherwise...
			else:
				# If the basic POS tags for the tagged and the gold standard token are different...
				if tagged_token.attrib["basic_pos"] != gold_token.attrib["basic_pos"]:
					# Increment the number of basic POS tagging errors by one
					basic_errors += 1
				# If the rich POS tags for the tagged and the gold standard token are different...
				if tagged_token.attrib["rich_pos"] != gold_token.attrib["rich_pos"]:
					# If a soft evaluation is being run...
					if leniency == "soft":
						# If the token is a noun but the gender is not the same, do nothing
						if tagged_token.attrib["basic_pos"] == "E" and gold_token.attrib["basic_pos"] == "E" and tagged_token.attrib["rich_pos"][-1:] == gold_token.attrib["rich_pos"][-1:]:
							pass
						# If the gold and tagged tokens' basic POS tags are both verb or pronoun, but one is tagged (rich POS) as singular and the other plural, do nothing
						elif (tagged_token.attrib["basic_pos"] == gold_token.attrib["basic_pos"] and (tagged_token.attrib["basic_pos"] == "Rha" or tagged_token.attrib["basic_pos"] == "B") and tagged_token.attrib["rich_pos"][-2:] == "ll" and gold_token.attrib["rich_pos"][-1:] == "u") or (tagged_token.attrib["basic_pos"] == gold_token.attrib["basic_pos"] and (tagged_token.attrib["basic_pos"] == "Rha" or tagged_token.attrib["basic_pos"] == "B") and tagged_token.attrib["rich_pos"][-1:] == "u" and gold_token.attrib["rich_pos"][-2:] == "ll"):
							pass
						# Otherwise...
						else:
							# Increment the number of rich POS tagging errors by one
							rich_errors += 1
					# Otherwise...
					else:
						# Increment the number of rich POS tagging errors by one
						rich_errors += 1
		# Print details about the numbers of errors and unknown tokens to the terminal
		print("From {} tokens:\n--- {} basic POS tag errors\n--- {} rich POS tag errors\n--- {} unknown tokens".format(len(tagged_tokens), basic_errors, rich_errors, unknown))
		# Calculate the precision, recall, and F1 score of CyTag considering only basic POS tags
		basic_precision = (((len(tagged_tokens) - unknown) - basic_errors) / (len(tagged_tokens) - unknown)) * 100
		basic_recall = ((((len(tagged_tokens) - unknown) - basic_errors)) / (((len(tagged_tokens) - unknown) - basic_errors) + unknown)) * 100
		basic_f = np.dot(2, ( np.dot(basic_precision, basic_recall) / (basic_precision + basic_recall) ))
		# Calculate the precision, recall, and F1 score of CyTag considering rich POS tags
		rich_precision = (((len(tagged_tokens) - unknown) - rich_errors) / (len(tagged_tokens) - unknown)) * 100
		rich_recall = ((((len(tagged_tokens) - unknown) - rich_errors)) / (((len(tagged_tokens) - unknown) - rich_errors) + unknown)) * 100
		rich_f = np.dot(2, ( np.dot(rich_precision, rich_recall) / (rich_precision + rich_recall) ))
		# Print details of the final evaluation statistics to the terminal
		print("\nFinal statistics {}considering only basic POS tags:\n--- precision: {}\n--- recall:    {}\n--- F1:        {}".format(" (soft evaluation) " if leniency == "soft" else "", round(basic_precision, 2), round(basic_recall, 2), round(basic_f, 2)))
		print("\nFinal statistics {}considering the rich POS tags:\n--- precision: {}\n--- recall:    {}\n--- F1:        {}".format(" (soft evaluation) " if leniency == "soft" else "", round(rich_precision, 2), round(rich_recall,2), round(rich_f, 2)))

if __name__ == '__main__':
	args = sys.argv[1:]
	# If there are three arguments, one text argument and two files...
	if len(args) == 3 and os.path.isfile(args[1]) == True and os.path.isfile(args[2]) == True:
		# If the text argument was not 'soft'...
		if args[0] != "soft":
			# Alert the user to the correct ordering and formatting for arguments
			print("ARGUMENT ERROR: 'soft' can be passed as a text flag when evaluate_cytag. Please check that the formatting of the passed arguments is as follows: The correct formatting of arguments is: 'soft' (optional) GOLD_CORPUS (required) TEST_CORPUS (required)")
		# Otherwise...
		else:
			# Run a 'soft' evaluation of the tagged CyTag output against the gold standard data
			evaluate("soft", args[1], args[2])
	# Or, if there are two further arguments, and both are files...
	elif len(args) == 2 and os.path.isfile(args[0]) == True and os.path.isfile(args[1]) == True:
		# Evaluate the tagged CyTag output against the gold standard data
		evaluate(None, args[0], args[1])
	# Otherwise...
	else:
		# Alert the user to the correct ordering and formatting for arguments
		print("ARGUMENT ERROR: Two XML-formatted output files should be passed as arguments in order to evalate CyTag. An optional 'soft' flag can also be passed for a more lenient evaluation. The correct formatting of arguments is: 'soft' (optional) GOLD_CORPUS (required) TEST_CORPUS (required)")