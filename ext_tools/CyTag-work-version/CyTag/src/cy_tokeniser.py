#!usr/bin/env python3
#-*- coding: utf-8 -*-
"""
'cy_tokeniser.py'

A tokeniser for Welsh texts.

Accepts as arguments:
	--- REQUIRED: A string of Welsh language text.
	or:
	--- REQUIRED: One or more Welsh input text files (raw text).

Returns:
	--- cy_taggedobject with input text segmented, sentences split, and tokenised.

Developed at Cardiff University as part of the CorCenCC project (www.corcencc.org).

2016-2017 Steve Neale <steveneale3000@gmail.com, NealeS2@cardiff.ac.uk>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses>.
"""

import sys
import os
import re

import json

from cy_taggedobject import taggedobject
from shared.create_folders import *
from cy_sentencesplitter import sentence_splitter
from shared.load_gazetteers import *

# Global dictionary for storing the CorCenCC gazetteers and global list for recording anonymised text sections
gazetteers = load_gazetteers()
anonymised_sections = []

# Global dictionary for storing known contractions and prefixes, loaded from an external .json file
contractions_and_prefixes = {}
with open("{}/../cy_gazetteers/contractions_and_prefixes.json".format(os.path.dirname(os.path.abspath(__file__)))) as contractionsprefixes_json:
	contractions_and_prefixes = json.load(contractionsprefixes_json)

def check_punctuation(token):
	try:
		# If the token has any anonymisation tags, return a list containing only the original token for now (it gets dealt with later in the corcencc_tokenise function)
		if token[:6] == "<anon>" or token[-7:] == "</anon>":
			return([token])
		# If: 
		#### no punctuation marks are found at the beginning or the end of the token
		##OR the token IS the punctuation mark
		##OR the token IS or is preceded by sequences of capital letters/numbers separated by dots
		##OR the token is in the abbreviations gazetteer 
		# then return a list containing only the original token
		elif len(re.findall("(^[.,:;\"\'!?<>{}()\]\[]|[.,:;\"\'!?<>{}()\]\[]$)", token)) < 1 or token in re.findall("(^[.,:;\"\'!?<>{}()\]\[]|[.,:;\"\'!?<>{}()\]\[]$)", token) or (len(re.findall("(?<![A-Z0-9_])([A-Z0-9_][.](\s*[A-Z0-9_][.])*)", token)) > 0 and (re.findall("(?<![A-Z0-9_])([A-Z0-9_][.](\s*[A-Z0-9_][.])*)", token)[0][0] == token)) or token in gazetteers["abbreviations"] or token in contractions_and_prefixes.keys():
			return([token])
		# If the token contains a sequence of 2 or more dots... 
		elif len(re.findall("[.]{2,}", token)) > 0:
			# If the token IS the sequence of 2 or more dots, return a list containing only the original token
			if re.findall("[.]{2,}", token)[0] == token:
				return([token])
			# Otherwise, split the ellipsis (sequence of dots) from the rest of the token, and return a list containing the rest of the token and the separated ellipsis
			else:
				ellipsis = re.findall("[.]{2,}", token)[0]
				return([token[:-len(ellipsis)], ellipsis])
		# Otherwise...
		else:
			# If any punctuation marks are found at the beginning or end of the token, split these into a list and remove and empty entries from that list 
			tokens = re.split("(^[.,:;\"\'!?<>{}()\]\[]|[.,:;\"\'!?<>{}()\]\[]$)", token)
			tokens = list(filter(None, tokens))
			# For each new token in the list, if the token is NOT in the acronyms gazetteer, recursively delete token and replace it with the results of this function (check_punctuation)
			for i, new_token in enumerate(tokens):
				if new_token not in gazetteers["acronyms"]:
					del tokens[i]
					tokens[i:i] = check_punctuation(new_token)
			# Return the list of tokens (split according to punctuation marks)
			return(tokens)
	# If anything went wrong, print the token to the terminal
	except:
		print("Error checking punctuation for token:", token)

def separate_elisions(token):
	# If the token has any anonymisation tags, return a list containing only the original token for now (it gets dealt with later in the corcencc_tokenise function)
	if token[:6] == "<anon>" or token[-7:] == "</anon>":
		return([token])
	# For each term in the list of contractions and prefixes...
	for term in contractions_and_prefixes.keys():
		# If the term is a contraction...
		if contractions_and_prefixes[term][0] == "contraction":
			# If the token begins with the term and the and the apostrophe appears at the end of the term, split the term and the token and return the two as separate tokens
			if term[-1:] == "'" and len(re.findall(r"^("+term+")", token)) > 0:
				separated = re.split(r"^("+term+")", token)
				separated = list(filter(None, separated))
				return(separated)
			# If the token ends with the term and the and the apostrophe appears at the beginning of the term, split the token and the term and return the two as separate tokens
			if term[:1] == "'" and len(re.findall(r"("+term+")$", token)) > 0:
				separated = re.split(r"("+term+")$", token)
				separated = list(filter(None, separated))
				return(separated)
	# Otherwise, return a list containing only the original token
	else:
		return([token])

def separate_symbols(token):
	# If the token has any anonymisation tags, return a list containing only the original token for now (it gets dealt with later in the corcencc_tokenise function)
	if token[:6] == "<anon>" or token[-7:] == "</anon>":
		return([token])
	# If any symbols of interest are part of the token (and the token is not a url containing either 'http' or 'www.'), split them into a list, remove and empty entries from the list, and return the split list
	if len(re.findall("([^\s^.,:;!?\-\'\"<>{}()\[\]^\w])", token)) > 0 and "http" not in token and "www." not in token: 
		separated = re.split("([^\s^.,;:!?\-\'\"<>{}()\[\]^\w])", token)
		separated = list(filter(None, separated))
		return(separated)
	# Otherwise, return a list containing only the original token
	else:
		return([token])

def corcencc_tokenise(sentence, total_tokens):
	# Create a new list to hold the tokens, and set the anonymisation start and end variables to the current number of total tokens
	tokens = []
	anon_start = anon_end = total_tokens
	# If the sentence is not empty...
	if sentence != "":
		# Split the tokens (using regex) by any whitespace that is not preceded or followed by a non-whitespace character followed by a fullstop.
		regexed_tokens = re.split("\s(?!\S[.])|(?<!\S[.])\s", sentence)
		# Remove any null values from the list of tokens
		tokens = list(filter(None, regexed_tokens))
		# For each token...
		for i, token in enumerate(tokens):
			# Check whether the token can be split into a group of tokens including punctuation marks
			checked_tokens = check_punctuation(token)
			# If the token was split, remove it and replace it with the list of tokens it was split into
			if len(checked_tokens) > 1:
				del tokens[i]
				tokens[i:i] = checked_tokens
		# For each token...
		for i, token in enumerate(tokens):
			# Check whether the token can be split into a group of tokens that were joined via elision
			separated_elisions = separate_elisions(token)
			# If the token was split, remove it and replace it with the list of tokens it was split into
			if len(separated_elisions) > 1:
				del tokens[i]
				tokens[i:i] = separated_elisions
		# For each token...
		for i, token in enumerate(tokens):
			# If the token contains a dash with something other than a digit either side of it...
			if "-" in token and token != "-" and not re.match("\d+(-)\d+", token):
				# Extract all of the prefixes from the list of known contractions and prefixes
				prefixes = [prefix for prefix in contractions_and_prefixes.keys() if contractions_and_prefixes[prefix][0] == "prefix"]
				# If the beginning of the token (up to the first hyphen) is not in the list of prefixes...
				if token[0:token.index("-")+1] not in prefixes and token[0:token.index("-")+1].lower() not in prefixes:
					# If there is a dash in the token, split the token (temporarily) on the dash
					if len(re.findall("(-)", token)) == 1:
						token_parts = token.split("-")
						# If both token parts begin with a capital letter, separate the token (permanently) by splitting on the dash
						if token_parts[0][0].isupper() and token_parts[1][0].isupper():
							separated_token = re.split("(-)", token)
							# If the token was split, remove it and replace it with the list of tokens it was split into
							if len(separated_token) > 1:
								del tokens[i]
								tokens[i:i] = separated_token
		# For each token...
		for i, token in enumerate(tokens):
			# Check whether the token can be split into a group of tokens including symbols
			separated_symbols = separate_symbols(token)
			# If the token was split, remove it and replace it with the list of tokens it was split into
			if len(separated_symbols) > 1:
				del tokens[i]
				tokens[i:i] = separated_symbols
		# For each token...
		for i, token in enumerate(tokens):
			# If the token starts AND ends with an anonymisation tag...
			if token[:6] == "<anon>" and token[-7:] == "</anon>":
				# Record the current token number as both the start and end point of the anonymised section
				anon_start = total_tokens + i+1
				anon_end = total_tokens + i+1
				# Extract the token without the tags
				token = token[6:-7]
				# Check whether the token can be split into a group of tokens including punctuation marks
				checked_tokens = check_punctuation(token)
				# If the token was split, remove it, add anonymistation tags to each of the tokens it was split into, replace the original token with the list of split tokens, and update the end point of the anonymised section accordingly 
				if len(checked_tokens) > 1:
					del tokens[i]
					checked_anon_tokens = []
					for checked_token in checked_tokens:
						checked_anon_tokens.append("<anon>{}</anon>".format(checked_token))
					tokens[i:i] = checked_anon_tokens
					anon_end = total_tokens + i + len(checked_tokens)
				# Extract the token without the tags
				token = tokens[i][6:-7]
				# Check whether the token can be split into a group of tokens that were joined via elision
				separated_elisions = separate_elisions(token)
				# If the token was split, remove it, add anonymistation tags to each of the tokens it was split into, replace the original token with the list of split tokens, and update the end point of the anonymised section accordingly 
				if len(separated_elisions) > 1:
					del tokens[i]
					separated_anon_elisions = []
					for separated_elision in separated_elisions:
						separated_anon_elisions.append("<anon>{}</anon>".format(separated_elision))
					tokens[i:i] = separated_anon_elisions
					anon_end = anon_end - 1 + len(separated_elisions)
				# Extract the token without the tags
				token = tokens[i][6:-7]
				# Check whether the token can be split into a group of tokens including symbols
				separated_symbols = separate_symbols(token)
				# If the token was split, remove it, add anonymistation tags to each of the tokens it was split into, replace the original token with the list of split tokens, and update the end point of the anonymised section accordingly 
				if len(separated_symbols) > 1:
					del tokens[i]
					separated_anon_symbols = []
					for separated_symbol in separated_symbols:
						separated_anon_symbols.append("<anon>{}</anon>".format(separated_symbol))
					tokens[i:i] = separated_anon_symbols
					anon_end = anon_end - 1 + len(separated_symbols)
				# Add the current start and end points to the list of anonymised sections
				anonymised_sections.append([anon_start, anon_end])
			# If the token starts OR ends with an anonymisation tag...
			if (token[:6] == "<anon>" and token[-7:] != "</anon>") or (token[:6] != "<anon>" and token[-7:] == "</anon>"):
				# If the token starts with an anonymisation tag...
				if token[:6] == "<anon>" and token[-7:] != "</anon>":
					# Record the current token number as the start point of the anonymised section
					anon_start = total_tokens + i+1
					# Remove the anonymisation tag from the start of the token
					token = token[6:]
					# Check whether the token can be split into a group of tokens including punctuation marks
					checked_tokens = check_punctuation(token)
					# If the token was split, remove it and replace it with the list of tokens it was split into
					if len(checked_tokens) > 1:
						del tokens[i]
						tokens[i:i] = checked_tokens
					# Set the test token back to the first token of any potential list of split tokens
					token = tokens[i]
					# Check whether the token can be split into a group of tokens that were joined via elision
					separated_elisions = separate_elisions(token)
					# If the token was split, remove it and replace it with the list of tokens it was split into
					if len(separated_elisions) > 1:
						del tokens[i]
						tokens[i:i] = separated_elisions
					# Set the test token back to the first token of any potential list of split tokens
					token = tokens[i]
					# Check whether the token can be split into a group of tokens including symbols
					separated_symbols = separate_symbols(token)
					# If the token was split, remove it and replace it with the list of tokens it was split into
					if len(separated_symbols) > 1:
						del tokens[i]
						tokens[i:i] = separated_symbols
				# If the token ends with an anonymisation tag...
				if token[:6] != "<anon>" and token[-7:] == "</anon>":
					# Record the current token number as the end point of the anonymised section
					anon_end = total_tokens + i+1
					# Remove the anonymisation tag from the end of the token
					token = token[:-7]
					# Check whether the token can be split into a group of tokens including punctuation marks
					checked_tokens = check_punctuation(token)
					# If the token was split, remove it, add anonymistation tags to the end of each of the tokens it was split into, replace the original token with the list of split tokens, and update the end point of the anonymised section accordingly
					if len(checked_tokens) > 1:
						del tokens[i]
						checked_anon_tokens = []
						for checked_token in checked_tokens:
							checked_anon_tokens.append("{}</anon>".format(checked_token))
						tokens[i:i] = checked_anon_tokens
						anon_end = total_tokens + i + len(checked_tokens)
					# Set the test token back to the original token minus the anonymisation tag at the end
					token = tokens[i][:-7]
					# Check whether the token can be split into a group of tokens that were joined via elision
					separated_elisions = separate_elisions(token)
					# If the token was split, remove it, add anonymistation tags to the end of each of the tokens it was split into, replace the original token with the list of split tokens, and update the end point of the anonymised section accordingly
					if len(separated_elisions) > 1:
						del tokens[i]
						separated_anon_elisions = []
						for separated_elision in separated_elisions:
							separated_anon_elisions.append("{}</anon>".format(separated_elision))
						tokens[i:i] = separated_anon_elisions
						anon_end = anon_end - 1 + len(separated_elisions)
					# Set the test token back to the original token minus the anonymisation tag at the end
					token = tokens[i][:-7]
					# Check whether the token can be split into a group of tokens including symbols
					separated_symbols = separate_symbols(token)
					# If the token was split, remove it, add anonymistation tags to the end of each of the tokens it was split into, replace the original token with the list of split tokens, and update the end point of the anonymised section accordingly
					if len(separated_symbols) > 1:
						del tokens[i]
						separated_anon_symbols = []
						for separated_symbol in separated_symbols:
							separated_anon_symbols.append("{}</anon>".format(separated_symbol))
						tokens[i:i] = separated_anon_symbols
						anon_end = anon_end - 1 + len(separated_symbols)
					# Add the current start and end points to the list of anonymised sections
					anonymised_sections.append([anon_start, anon_end])
		# For each token, remove any anonymisation tags that are still present 
		for i, token in enumerate(tokens):
			if token[:6] == "<anon>":
				token = token[6:]
			if token[-7:] == "</anon>":
				token = token[:-7]
			tokens[i] = token
	# Return the list of tokens
	return(tokens)

def tokenise(sentencesplit_files):
	# Create an empty list to hold the split tokens
	split_tokens = []
	# Create variables to store the total numbers of sentences and tokens
	total_sentences, total_tokens = 0, 0
	# For each sentence split file passed to the tokenise function...
	for file_id, file in enumerate(sentencesplit_files):
		# Append an empty list to the list of split tokens
		split_tokens.append([])
		# For each segment in this file...
		for segment_id, segment in enumerate(file[2]):
			# Append an empty list to the appropriate file in the wider split tokens list
			split_tokens[file_id].append([])
			# For each sentence in this segment...
			for sentence_id, sentence in enumerate(segment[1]):
				total_sentences += 1
				# If the last character is a full stop but it's not preceded by a space, add a space in before the full stop
				if sentence[-1:] == "." and sentence[-2:] != " .":
					sentence = "{}{}".format(sentence[:-1], " .")
				# Run the corcencc_tokenise function over the sentence to return a list of tokens
				tokens = corcencc_tokenise(sentence, total_tokens)
				# Create separate arrays of start and end points for anonymised sections
				anon_starts = [x[0] for x in anonymised_sections]
				anon_ends = [x[1] for x in anonymised_sections]
				# Create start and end variables
				start, end = 0, 0
				# For each token in the list...
				for token_id, token in enumerate(tokens):
					# Replace the token itself with a list, containing the token and a dictionary to hold attributes about it
					tokens[token_id] = [token, {}]
					# If the current token is in the array of start points for anonymised sections, set the start and end variables to the appropriate index in the start and end point arrays
					if (total_tokens + token_id+1) in anon_starts:
						start = anon_starts[anon_starts.index(total_tokens + token_id+1)]
						end = anon_ends[anon_starts.index(total_tokens + token_id+1)]
					# If the token number is greater than the end variable and the end variable is not 0, reset the start variable to 0
					if (total_tokens + token_id+1 > end and end != 0):
						start = 0
					# Attach keys for the 'location' (within the cy_taggedobject structure) and 'position' (sentence,token) of the token to its attribute dictionary
					tokens[token_id][1]["location"] = [file_id, segment_id, sentence_id]
					tokens[token_id][1]["position"] = "{},{}".format(total_sentences, token_id+1)
					# If the token number is greater than or equal to the start variable and the start variable is not 0, attach an 'anon' key with a value of 'true' to the token's attribute dictionary
					if (total_tokens + token_id+1 >= start and start != 0):
						tokens[token_id][1]["anon"] = "true"	
				# Increment the total number of tokens by the number of tokens in this sentence
				total_tokens += len(tokens)
				# Add the tokens to the appropriate segment in the appropriate file in the wider split tokens list
				split_tokens[file_id][segment_id].append(tokens)
	# Return the list of split tokens
	return(split_tokens)

def tokeniser(input_data, output):
	# Split the input data into a sentence split output object
	output = sentence_splitter(input_data, output)
	# Produce a list of tokens from the sentence split output object
	tokens = tokenise(output.files)
	# Store the list of sentences in the output object
	output.store_tokens(tokens)
	# Return the output object
	return(output)

if __name__ == "__main__":
	args = sys.argv[1:]
	# If there was only one argument provided and it was not a file...
	if len(args) == 1 and os.path.isfile(args[0]) != True:
		# Run the tokeniser
		tokeniser(args[0], taggedobject())
	#Otherwise:
	else:
		# Run the tokeniser
		tokeniser(args, taggedobject())