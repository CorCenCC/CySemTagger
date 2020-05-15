#!usr/bin/env python3
#-*- coding: utf-8 -*-
"""
'cy_sentencesplitter.py'

A sentence splitter for Welsh texts.

Accepts as arguments:
	--- REQUIRED: A string of Welsh language text.
	or:
	--- REQUIRED: One or more Welsh input text files (raw text).

Returns:
	--- cy_taggedobject with input text segmented and sentences split.

Developed at Cardiff University as part of the CorCenCC project (www.corcencc.org).

2016-2017 Steve Neale <steveneale3000@gmail.com, NealeS2@cardiff.ac.uk>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses>.
"""

import sys
import os
import re

from cy_taggedobject import taggedobject
from shared.create_folders import *
from cy_textsegmenter import segment_text
from shared.load_gazetteers import *

def split_sentences(segmented_files):
	# Create an empty list to hold the split sentences
	split_sentences = []
	# Load the appropriate gazetteers
	gazetteers = load_gazetteers()
	# For each segmented file passed to the split_sentences function...
	for file_id, file in enumerate(segmented_files):
		# Append an empty list to the list of split sentences
		split_sentences.append([])
		# For each segment in this file...
		for segment in file[2]:
			# Split the given segment into sentences based on a regex pattern - whitespace preceded by certain punctuation marks, but not by certain combinations of letters and punctuation marks or by any of the negative lookbehind assertions created for the 'abbreviations' gazetteer
			pattern = gazetteers["abbreviations_regex"] + "(?<=[.|!|?])(?<!\s[A-Z][.])(?<![A-Z][.][A-Z][.])(?<![.]\s[.])(?<![.][.])[\s]"
			sentences = re.split(pattern, segment)
			# Create a variable 'k' and iterate through the split sentences...
			k = 0
			while k < len(sentences):
				# If an empty sentence is encountered, delete it
				if sentences[k] == "":
					del sentences[k] 
				else:
					# If we are not on the last sentence...
					if k < len(sentences)-1:
						# If the next sentence splits according to the regex pattern...
						if re.match(pattern, sentences[k+1]):
							# Append the next sentence to the current one and then delete it
							sentences[k] = sentences[k] + sentences[k+1].strip()
							del sentences[k+1]
					k+=1
			# Append the split sentences to the appropriate file in the wider split sentences list
			split_sentences[file_id].append(sentences)
	# Return the list of split sentences
	return(split_sentences)

def sentence_splitter(input_data, output):
	# Split the input data into a text segmented output object
	output = segment_text(input_data, output)
	# Produce a list of sentences from the text segmented output object
	sentences = split_sentences(output.files)
	# Store the list of sentences in the output object
	output.store_sentences(sentences)
	# Return the output object
	return(output)

if __name__ == "__main__":
	args = sys.argv[1:]
	# If there was only one argument provided and it was not a file...
	if len(args) == 1 and os.path.isfile(args[0]) != True:
		# Run the sentence splitter treating the argument as a single string of text
		sentence_splitter(args[0], taggedobject())
	#Otherwise:
	else:
		# Run the sentence splitter treating the arguments as input files
		sentence_splitter(args, taggedobject())