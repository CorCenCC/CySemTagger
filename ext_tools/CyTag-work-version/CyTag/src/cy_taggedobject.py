#!usr/bin/env python3
#-*- coding: utf-8 -*-
"""
'cy_taggedobject.py'

A class for storing and manipulating information about CyTag output as it is passed through various stages of the overall pipeline (text segmentation -> sentence splitting -> tokenisation -> part-of-speech (POS) tagging).

Developed at Cardiff University as part of the CorCenCC project (www.corcencc.org).

2016-2017 Steve Neale <steveneale3000@gmail.com, NealeS2@cardiff.ac.uk>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses>.
"""

import sys
import os

try:
	from lxml import etree
except ImportError:
	pass

from shared.create_folders import *

class taggedobject:
	def __init__(self):
		# Create an empty list to store files
		self.files = []

	# Create new variables for the total numbers of files, segments (paragraphs), sentences, and tokens in the tagged object
	total_files = 0
	total_segments = 0
	total_sentences = 0
	total_tokens = 0

	def store_segments(self, lines):
		# For each file in a set of lines...
		for file in lines:
			# Increment the total number of files by 1 
			self.total_files += 1
			# Increment the total number of segments by the number of separated segments in the file
			self.total_segments += len(file[1])
			# Append the file name, number of segments and the segments themselves to the list of files
			self.files.append([file[0], # File name
								len(file[1]), # Total number of segments in this file
								file[1]]) # Separated segments (paragraphs)

	def store_sentences(self, split_sentences):
		# For each file in the list of files in this tagged object...
		for file_id, file in enumerate(self.files):
			# Replace the list of seperated segments with the list of split sentences (organised by segment) passed in for this file
			file[2] = split_sentences[file_id]
			# For each (now sentence split) segment in this file...
			for segment_id, segment in enumerate(file[2]):
				# Replace the sentence split segment with the number of sentences in the segment as well as the sentence split segment itself
				file[2][segment_id] = [len(segment), segment]
				# Increment the total number of sentences by the length of the sentence split segment
				self.total_sentences += len(segment)

	def store_tokens(self, tokens):
		# For each file in the list of files in this tagged object...
		for file_id, file in enumerate(self.files):
			# For each sentence split segment in this file...
			for segment_id, segment in enumerate(file[2]):
				# For each sentence in this segment...
				for sentence_id, sentence in enumerate(segment[1]):
					# Find the appropriate tokens for this sentence from the list of passed tokens
					sentence_tokens = tokens[file_id][segment_id][sentence_id]
					# Replace the sentence with the number of tokens in the sentence as well as the tokenised sentence itself
					segment[1][sentence_id] = [len(sentence_tokens), sentence_tokens]
					# Increment the total number of tokens by the number of tokens in the sentence
					self.total_tokens += len(sentence_tokens)

	def store_tags(self, tagged_tokens):
		# For each token in the list of passed (tagged) tokens...
		for token_id, token in enumerate(tagged_tokens):
			# If the token is the first token in the sentence...
			if token[2].split(",")[1] == "1":
				# Add a new list to the appropriate sentence in this tagged object
				self.files[token[1][0]][2][token[1][1]][1][token[1][2]][1] = []
				# Append the passed (tagged) token to the appropriate sentence in this tagged object
				self.files[token[1][0]][2][token[1][1]][1][token[1][2]][1].append(token)
			# Otherwise...
			else:
				# Append the passed (tagged) token to the appropriate sentence in this tagged object
				self.files[token[1][0]][2][token[1][1]][1][token[1][2]][1].append(token)

	def print_to_stdout(self):
		# Create a variable to store the total number of tokens
		total_tokens = 0
		# For each file in the list of files in this tagged object...
		for file_id, file in enumerate(self.files):
			# For each sentence split segment in this file...
			for segment_id, segment in enumerate(file[2]):
				# For each sentence in this segment...
				for sentence_id, sentence in enumerate(segment[1]):
					# For each token in this sentence...
					for token_id, token in enumerate(sentence[1]):
						# Increment the total number of tokens by 1
						total_tokens += 1
						# Create variables for the lemma, basic and rich POS tags, and position of the token
						lemma, basic_pos, rich_pos, position = token[3], token[4], token[5], token[2]
						# If mutation information is included with the token, create a variable for it
						mutation = "+{}".format(token[6]) if len(token) == 7 else ""
						# Print tab-separated information about the token to standard output
						print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(total_tokens, token[0], position, lemma, basic_pos, rich_pos, mutation))

	def print_to_file(self, output_name, directory, output_format):
		# Create the necessary folders to store output files
		folders = create_folders([[], output_name, directory])
		# If any kind of warning of message was returned while creating folders, print it and then return
		if folders != None:
			print(folders)
			return
		# Create variables to store the total number of segments, sentences, and tokens
		total_segments, total_sentences, total_tokens = 0, 0, 0
		# Create variables to to store the lxml element tree or the TSV-formatted output file
		corpus_element, tsv_output = None, None
		# If an XML output file is needed...
		if output_format in ["xml", "all"]:
			# Create an lxml element for the corpus and add its name to it as an attribute
			corpus_element = etree.Element("corpus")
			corpus_element.attrib["name"] = output_name
		# If a TSV output file is needed, create it in the appropriate location
		if output_format in ["tsv", "all"]:
			tsv_output = open("{}/../{}/{}/{}.tsv".format(os.path.dirname(os.path.abspath(__file__)), "outputs", directory if directory != None else output_name, output_name), "w")
		# For each file in the list of files in this tagged object...
		for file_id, file in enumerate(self.files):
			# Create variables to store the number of sentences and number of tokens in this file
			file_sentences, file_tokens = 0, 0
			# If an XML output file is needed, print the opening tag for this file
			file_element = None
			if output_format in ["xml", "all"]:
				# Create an lxml element for the file and add the relevant details to it as attributes
				file_element = etree.Element("file")
				file_element.attrib["id"] = str(file_id+1)
				file_element.attrib["name"] = os.path.basename(file[0])
			# For each sentence split segment in this file...
			for segment_id, segment in enumerate(file[2]):
				# Increment the total number of segments (paragraphs) by 1
				total_segments += 1
				# If an XML output file is needed...
				paragraph_element = None
				if output_format in ["xml", "all"]:
					# Create an lxml element for the paragraph and add the relevant details to it as attributes
					paragraph_element = etree.Element("paragraph")
					paragraph_element.attrib["id"] = str(total_segments)
					paragraph_element.attrib["file_id"] = str(segment_id+1)
				# For each sentence in this segment...
				for sentence_id, sentence in enumerate(segment[1]):
					# Increment the total number of sentences and the number of sentences in this file by 1
					total_sentences += 1
					file_sentences += 1
					# If an XML output file is needed...
					sentence_element = None
					if output_format in ["xml", "all"]:
						# Create an lxml element for the sentence and add the relevant details to it as attributes
						sentence_element = etree.Element("sentence")
						sentence_element.attrib["id"] = str(total_sentences)
						sentence_element.attrib["file_id"] = str(file_sentences)
						sentence_element.attrib["para_id"] = str(sentence_id+1)
					# For each token in this sentence...
					for token_id, token in enumerate(sentence[1]):
						# Increment the total number of tokens and the number of tokens in this file by 1
						total_tokens += 1
						file_tokens += 1
						# Create variables to store the lemma, basic POS tag and rich POS tag for this token
						lemma, basic_pos, rich_pos = "", "", ""
						# Create a variable to store the position for this token
						position = token[2] if len(token) > 2 else "{},{}".format(total_sentences, token_id+1)
						# If there are more than 3 values in this token, use these values to populate the lemma, basic POS tag and rich POS tag variables
						if len(token) > 3:
							lemma, basic_pos, rich_pos = token[3], token[4], token[5]
						# If an XML output file is needed...
						token_element = None
						if output_format in ["xml", "all"]:
							# Create an lxml element for the token and add the relevant details to it as attributes
							token_element = etree.Element("token")
							token_element.attrib["id"] = str(total_tokens)
							token_element.attrib["file_id"] = str(file_tokens)
							token_element.attrib["sent_id"] = str(token_id+1)
							token_element.attrib["lemma"] = lemma
							token_element.attrib["basic_pos"] = basic_pos
							token_element.attrib["rich_pos"] = rich_pos
							if len(token) == 7:
								token_element.attrib["mutation"] = token[6]
							token_element.attrib["position"] = position
							token_element.text = token[0]
							sentence_element.append(token_element)
						# If a TSV output file is needed...
						if output_format in ["tsv", "all"]:
							# If the token has 7 values, create a variable to hold mutation details for this token
							mutation = "+{}".format(token[6]) if len(token) == 7 else ""
							# Print details of the token to the TSV-formatted output file
							print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(total_tokens, token[0], position, lemma, basic_pos, rich_pos, mutation), file=tsv_output)
		# If an XML output file is needed, append the appropriate XML elements to each other and print the final lxml tree
					if output_format in ["xml", "all"]:
						paragraph_element.append(sentence_element)	
				if output_format in ["xml", "all"]:
					file_element.append(paragraph_element)		
			if output_format in ["xml", "all"]:
				corpus_element.append(file_element)
		if output_format in ["xml", "all"]:
			tree = etree.ElementTree(corpus_element)
			tree.write("{}/../{}/{}/{}.xml".format(os.path.dirname(os.path.abspath(__file__)), "outputs", directory if directory != None else output_name, output_name), pretty_print=True, xml_declaration=True, encoding='UTF-8')


