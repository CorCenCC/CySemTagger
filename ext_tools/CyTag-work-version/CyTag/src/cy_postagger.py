#!usr/bin/env python3
#-*- coding: utf-8 -*-
"""
'cy_postagger.py'

A part-of-speech (POS) tagger for Welsh texts.

Accepts as arguments:
	--- REQUIRED: A string of Welsh language text.
	or:
	--- REQUIRED: One or more Welsh input text files (raw text).
	--- REQUIRED: A name to describe the corpus and its output files.
	--- OPTIONAL: A directory in which output files will be saved.
	--- OPTIONAL: A flag ('print') to let cy_postagger know whether to write CG-formatted readings files to the output folder or not.

Returns:
	--- cy_taggedobject with input text segmented, sentences split, tokenised, and POS tagged.

Developed at Cardiff University as part of the CorCenCC project (www.corcencc.org).

2016-2017 Steve Neale <steveneale3000@gmail.com, NealeS2@cardiff.ac.uk>, Kevin Donnelly <kevin@dotmon.com>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses>.
"""

import sys
import os
import re
import subprocess

import json

try:
	from progress.bar import Bar
except ImportError:
	pass

from cy_taggedobject import taggedobject
from shared.check_libraries import *
from shared.create_folders import *
from cy_tokeniser import tokeniser
from shared.load_gazetteers import *
from shared.load_lexicon import *

# Find and store the location of VISL CG-3
vislcg3_location = subprocess.Popen(["which", "vislcg3"], stdout=subprocess.PIPE).communicate()[0].strip()

# Global dictionaries for storing the CorCenCC gazetteers and the pre-formatted CorCenCC lexicon
gazetteers = load_gazetteers()
corcencc_lexicon = load_lexicon()

# Global dictionary for storing known contractions and prefixes, loaded from an external .json file
contractions_and_prefixes = {}
with open("{}/../cy_gazetteers/contractions_and_prefixes.json".format(os.path.dirname(os.path.abspath(__file__)))) as contractionsprefixes_json:
	contractions_and_prefixes = json.load(contractionsprefixes_json)

# A simple swith to use the 'check_coverage' options when tagging (i.e. guess untagged words using entries in the tag-token coverage and tag-sequence dictionaries)
# NOTE: Leave this as True, unless producing tagged output for making new tag-token coverage and tag-sequence dictionaries
check_coverage = True
#check_coverage = False

# Load the CyTag tag-token coverage dictionary from an external .json file
cy_coverage = {}
with open("{}/../lexicon/{}".format(os.path.dirname(os.path.abspath(__file__)), "CyTag_tag-token_coverage")) as coverage_file:
	cy_coverage = json.load(coverage_file)

# Load the CyTag tag-sequence dictionary from an external .json file
cy_tagsequences = {}
with open("{}/../lexicon/{}".format(os.path.dirname(os.path.abspath(__file__)), "CyTag_tag-sequences")) as tagsequence_file:
	cy_tagsequences = json.load(tagsequence_file)

# A tag categories table, storing the appropriate rich POS tags that collapse into each basic POS tag
tag_categories = [["E", ["Egu", "Ebu", "Egll", "Ebll", "Egbu", "Egbll", "Ep", "Epg", "Epb"]],
					["Ar", ["Arsym", "Ar1u", "Ar2u", "Ar3gu", "Ar3bu", "Ar1ll", "Ar2ll", "Ar3ll"]],
					["Cys", ["Cyscyd", "Cysis"]],
					["Rhi", ["Rhifol", "Rhifold", "Rhifolt", "Rhitref", "Rhitrefd", "Rhitreft"]],
					["Ans", ["Anscadu", "Anscadbu", "Anscadll", "Anscyf", "Anscym", "Anseith"]],
					["B", ["Be", "Bpres1u", "Bpres2u", "Bpres3u", "Bpres1ll", "Bpres2ll", "Bpres3ll", "Bpresamhers", "Bpres3perth", "Bpres3amhen",
							"Bdyf1u", "Bdyf2u", "Bdyf3u", "Bdyf1ll", "Bdyf2ll", "Bdyf3ll", "Bdyfamhers",
							"Bgorb1u", "Bgorb2u", "Bgorb3u", "Bgorb1ll", "Bgorb2ll", "Bgorb3ll", "Bgorbamhers",
							"Bamherff1u", "Bamherff2u", "Bamherff3u", "Bamherff1ll", "Bamherff2ll", "Bamherff3ll", "Bamherffamhers",
							"Bgorff1u", "Bgorff2u", "Bgorff3u", "Bgorff1ll", "Bgorff2ll", "Bgorff3ll", "Bgorffamhers", "Bgorffsef",
							"Bgorch2u", "Bgorch3u", "Bgorch1ll", "Bgorch2ll", "Bgorch3ll", "Bgorchamhers",
							"Bdibdyf1u", "Bdibdyf2u", "Bdibdyf3u", "Bdibdyf1ll", "Bdibdyf2ll", "Bdibdyf3ll", "Bdibdyfamhers",
							"Bamod1u", "Bamod2u", "Bamod3u", "Bamod1ll", "Bamod2ll", "Bamod3ll", "Bamodamhers"]],
					["Rha", ["Rhapers1u", "Rhapers2u", "Rhapers3gu", "Rhapers3bu", "Rhapers1ll", "Rhapers2ll", "Rhapers3ll",
							"Rhadib1u", "Rhadib2u", "Rhadib3gu", "Rhadib3bu", "Rhadib1ll", "Rhadib2ll", "Rhadib3ll",
							"Rhamedd1u", "Rhamedd2u", "Rhamedd3gu", "Rhamedd3bu", "Rhamedd1ll", "Rhamedd2ll", "Rhamedd3ll",
							"Rhacys1u", "Rhacys2u", "Rhacys3gu", "Rhacys3bu", "Rhacys1ll", "Rhacys2ll", "Rhacys3ll",
							"Rhagof", "Rhadangg", "Rhadangb", "Rhadangd", "Rhaperth", "Rhaatb", "Rhacil"]],
					["U", ["U", "Uneg", "Ucad", "Ugof", "Utra", "Uberf"]],
					["Gw", ["Gwest", "Gwfform", "Gwsym", "Gwacr", "Gwtalf", "Gwdig", "Gwllyth", "Gwann"]],
					["Atd", ["Atdt", "Atdcan", "Atdchw", "Atdde", "Atdcys", "Atddyf"]],
					["YFB", ["YFB"]],
					["Adf", ["Adf"]],
					["Ebych", ["Ebych"]]]

# A table, storing the appropriate morphological elements that make up each rich POS tag
morphological_table = [["Egu", ["E", "g", "u"]],
						["Ebu", ["E", "b", "u"]],
						["Egll", ["E", "g", "ll"]],
						["Ebll", ["E", "b", "ll"]],
						["Egbu", ["E", "gb", "u"]],
						["Egbll", ["E", "gb", "ll"]],
						["Ep", ["E", "p"]],
						["Epg", ["E", "p", "g"]],
						["Epb", ["E", "p", "b"]],
						["Arsym", ["Ar", "sym"]],
						["Ar1u", ["Ar", "1", "u"]],
						["Ar2u", ["Ar", "2", "u"]],
						["Ar3gu", ["Ar", "3", "g", "u"]],
						["Ar3bu", ["Ar", "3", "b", "u"]],
						["Ar1ll", ["Ar", "1", "ll"]],
						["Ar2ll", ["Ar", "2", "ll"]],
						["Ar3ll", ["Ar", "3", "ll"]],
						["Cyscyd", ["Cys", "cyd"]],
						["Cysis", ["Cys", "is"]],
						["Rhifol", ["Rhi", "fol"]],
						["Rhifold", ["Rhi", "fol", "d"]],
						["Rhifolt", ["Rhi", "fol", "t"]],
						["Rhitref", ["Rhi", "tref"]],
						["Rhitrefd", ["Rhi", "tref", "d"]],
						["Rhitreft", ["Rhi", "tref", "t"]],
						["Anscadu", ["Ans", "cad", "u"]],
						["Anscadbu", ["Ans", "cad", "b", "u"]],
						["Anscadll", ["Ans", "cad", "ll"]],
						["Anscyf", ["Ans", "cyf"]],
						["Anscym", ["Ans", "cym"]],
						["Anseith", ["Ans", "eith"]],
						["Be", ["B", "e"]],
						["Bpres1u", ["B", "pres", "1", "u"]],
						["Bpres2u", ["B", "pres", "2", "u"]],
						["Bpres3u", ["B", "pres", "3", "u"]],
						["Bpres1ll", ["B", "pres", "1", "ll"]],
						["Bpres2ll", ["B", "pres", "2", "ll"]],
						["Bpres3ll", ["B", "pres", "3", "ll"]],
						["Bpresamhers", ["B", "pres", "amhers"]],
						["Bpres3perth", ["B", "pres", "3", "perth"]],
						["Bpres3amhen", ["B", "pres", "3", "amhen"]],
						["Bdyf1u", ["B", "dyf", "1", "u"]],
						["Bdyf2u", ["B", "dyf", "2", "u"]],
						["Bdyf3u", ["B", "dyf", "3", "u"]],
						["Bdyf1ll", ["B", "dyf", "1", "ll"]],
						["Bdyf2ll", ["B", "dyf", "2", "ll"]],
						["Bdyf3ll", ["B", "dyf", "3", "ll"]],
						["Bdyfamhers", ["B", "dyf", "amhers"]],
						["Bgorb1u", ["B", "gorb", "1", "u"]],
						["Bgorb2u", ["B", "gorb", "2", "u"]],
						["Bgorb3u", ["B", "gorb", "3", "u"]],
						["Bgorb1ll", ["B", "gorb", "1", "ll"]],
						["Bgorb2ll", ["B", "gorb", "2", "ll"]],
						["Bgorb3ll", ["B", "gorb", "3", "ll"]],
						["Bgorbamhers", ["B", "gorb", "amhers"]],
						["Bamherff1u", ["B", "amherff", "1", "u"]],
						["Bamherff2u", ["B", "amherff", "2", "u"]],
						["Bamherff3u", ["B", "amherff", "3", "u"]],
						["Bamherff1ll", ["B", "amherff", "1", "ll"]],
						["Bamherff2ll", ["B", "amherff", "2", "ll"]],
						["Bamherff3ll", ["B", "amherff", "3", "ll"]],
						["Bamherffamhers", ["B", "amherff", "amhers"]],
						["Bgorff1u", ["B", "gorff", "1", "u"]],
						["Bgorff2u", ["B", "gorff", "2", "u"]],
						["Bgorff3u", ["B", "gorff", "3", "u"]],
						["Bgorff1ll", ["B", "gorff", "1", "ll"]],
						["Bgorff2ll", ["B", "gorff", "2", "ll"]],
						["Bgorff3ll", ["B", "gorff", "3", "ll"]],
						["Bgorffamhers", ["B", "gorff", "amhers"]],
						["Bgorffsef", ["B", "gorch", "sef"]],
						["Bgorch2u", ["B", "gorch", "2", "u"]],
						["Bgorch3u", ["B", "gorch", "3", "u"]],
						["Bgorch1ll", ["B", "gorch", "1", "ll"]],
						["Bgorch2ll", ["B", "gorch", "2", "ll"]],
						["Bgorch3ll", ["B", "gorch", "3", "ll"]],
						["Bgorchamhers", ["B", "gorch", "amhers"]],
						["Bdibdyf1u", ["B", "dibdyf", "1", "u"]],
						["Bdibdyf2u", ["B", "dibdyf", "2", "u"]],
						["Bdibdyf3u", ["B", "dibdyf", "3", "u"]],
						["Bdibdyf1ll", ["B", "dibdyf", "1", "ll"]],
						["Bdibdyf2ll", ["B", "dibdyf", "2", "ll"]],
						["Bdibdyf3ll", ["B", "dibdyf", "3", "ll"]],
						["Bdibdyfamhers", ["B", "dibdyf", "amhers"]],
						["Bamod1u", ["B", "amod", "1", "u"]],
						["Bamod2u", ["B", "amod", "2", "u"]],
						["Bamod3u", ["B", "amod", "3", "u"]],
						["Bamod1ll", ["B", "amod", "1", "ll"]],
						["Bamod2ll", ["B", "amod", "2", "ll"]],
						["Bamod3ll", ["B", "amod", "3", "ll"]],
						["Bamodamhers", ["B", "amod", "amhers"]],
						["Rhapers1u", ["Rha", "pers", "1", "u"]],
						["Rhapers2u", ["Rha", "pers", "2", "u"]],
						["Rhapers3gu", ["Rha", "pers", "3", "g", "u"]],
						["Rhapers3bu", ["Rha", "pers", "3", "b", "u"]],
						["Rhapers1ll", ["Rha", "pers", "1", "ll"]],
						["Rhapers2ll", ["Rha", "pers", "2", "ll"]],
						["Rhapers3ll", ["Rha", "pers", "3", "ll"]],
						["Rhadib1u", ["Rha", "dib", "1", "u"]],
						["Rhadib2u", ["Rha", "dib", "2", "u"]],
						["Rhadib3gu", ["Rha", "dib", "3", "g", "u"]],
						["Rhadib3bu", ["Rha", "dib", "3", "b", "u"]],
						["Rhadib1ll", ["Rha", "dib", "1", "ll"]],
						["Rhadib2ll", ["Rha", "dib", "2", "ll"]],
						["Rhadib3ll", ["Rha", "dib", "3", "ll"]],
						["Rhamedd1u", ["Rha", "medd", "1", "u"]],
						["Rhamedd2u", ["Rha", "medd", "2", "u"]],
						["Rhamedd3gu", ["Rha", "medd", "3", "g", "u"]],
						["Rhamedd3bu", ["Rha", "medd", "3", "b", "u"]],
						["Rhamedd1ll", ["Rha", "medd", "1", "ll"]],
						["Rhamedd2ll", ["Rha", "medd", "2", "ll"]],
						["Rhamedd3ll", ["Rha", "medd", "3", "ll"]],
						["Rhacys1u", ["Rha", "cys", "1", "u"]],
						["Rhacys2u", ["Rha", "cys", "2", "u"]],
						["Rhacys3gu", ["Rha", "cys", "3", "g", "u"]],
						["Rhacys3bu", ["Rha", "cys", "3", "b", "u"]],
						["Rhacys1ll", ["Rha", "cys", "1", "ll"]],
						["Rhacys2ll", ["Rha", "cys", "2", "ll"]],
						["Rhacys3ll", ["Rha", "cys", "3", "ll"]],
						["Rhagof", ["Rha", "gof"]],
						["Rhadangg", ["Rha", "dang", "g"]],
						["Rhadangb", ["Rha", "dang", "b"]],
						["Rhadangd", ["Rha", "dang", "d"]],
						["Rhaperth", ["Rha", "perth"]],
						["Rhaatb", ["Rha", "atb"]],
						["Rhacil", ["Rha", "cil"]],
						["Uneg", ["U", "neg"]],
						["Ucad", ["U", "cad"]],
						["Ugof", ["U", "gof"]],
						["Utra", ["U", "tra"]],
						["Uberf", ["U", "berf"]],
						["Gwest", ["Gw", "est"]],
						["Gwfform", ["Gw", "fform"]],
						["Gwsym", ["Gw", "sym"]],
						["Gwacr", ["Gw", "acr"]],
						["Gwtalf", ["Gw", "talf"]],
						["Gwdig", ["Gw", "dig"]],
						["Gwllyth", ["Gw", "llyth"]],
						["Gwann", ["Gw", "ann"]],
						["Atdt", ["Atd", "t"]],
						["Atdcan", ["Atd", "can"]],
						["Atdchw", ["Atd", "chw"]],
						["Atdde", ["Atd", "de"]],
						["Atdcys", ["Atd", "cys"]],
						["Atdyf", ["Atd", "dyf"]]]

########################################################################
# Find and return definitely identifiable tags for a token, including: #
#	--- punctuation													   #
#	--- symbols														   #
#	--- digits 														   #
#	--- acronynms or abbreviations (from gazetteers) 				   #
########################################################################

def find_definite_tags(token):
	# Create an empty variable for the POS tag
	pos = ""
	# If the token is one of a selection of punctuation marks, assign the correct POS tags (formatted basic_tag:rich_tag) to it depending on whether it's a final, medial, left, right, hyphen or quotation mark
	if re.match(r"[.,:;\"\'!?\-\—<>{}\[\]()]", token):
		if re.match(r"[.!?]", token):
			pos = "Atd:Atdt"
		if re.match(r"[,;:—]", token):
			pos = "Atd:Atdcan"
		if re.match(r"[<{\[(]", token):
			pos = "Atd:Atdchw"
		if re.match(r"[>}\])]", token):
			pos = "Atd:Atdde"
		if token is "-":
			pos = "Atd:Atdcys"
		if token is "\'" or token is "\"":
			pos = "Atd:Atdyf"	
	# If the token is not whitespace, is not one of the punctuation marks and is not a character, assign the the correct POS tags for a symbol
	if re.match(r"[^\s^.,:;!?\-\—\'\"<>{}\[\]()^\w]", token):
		pos = "Gw:Gwsym"
	# If the token is a sequence of digits, assign the correct POS tags for a digit
	if re.match(r"^-?[0-9]+$", token):
		pos = "Gw:Gwdig"
	# If no POS tag has yet been assigned and the token is in either the 'acronynms' or 'abbreviations' gazetteers, assign the appropriate POS tag
	if pos == "" and token in gazetteers["acronyms"]:
		pos = "Gw:Gwacr"
	if pos == "" and token.lower() in gazetteers["abbreviations"]:
		pos = "Gw:Gwtalf"
	# Return the POS tag
	return pos

#####################################################################
# Lookup readings for a given token in the lexicon, and return them #
#####################################################################

def lookup_readings(token):
	# Create an empty list to hold the readings
	readings = []
	# If the token is in the lexicon (of if the lower-cased version of the token is in the lexicon), format each entry of the token found in the lexicon and add it to the list of readings
	if token in corcencc_lexicon:
		readings = [[token, [tag_morphology(x["pos_enriched"])], x["lemma"], [x["lemma_en"]], ""] for x in corcencc_lexicon[token]]
	elif token.lower() in corcencc_lexicon:
		readings = [[token.lower(), [tag_morphology(x["pos_enriched"])], x["lemma"], [x["lemma_en"]], ""] for x in corcencc_lexicon[token.lower()]]
	# Find a list of possible mutations for the input token
	possible_mutations = lookup_mutation(token)
	# If the list of possible mutations is greater than 0...
	if len(possible_mutations) > 0:
		# If any of the mutations are in the lexicon, format each entry for the mutation found in the lexicon and add it to the list of readings
		for mutation in possible_mutations:
			if mutation[0] in corcencc_lexicon:
				mutation_readings = [[mutation[0], [tag_morphology(x["pos_enriched"])], x["lemma"], [x["lemma_en"]], mutation[1]] for x in corcencc_lexicon[mutation[0]]]
				readings = readings + mutation_readings
	# Return the list of readings
	return readings

########################################################################################
# Lookup readings for multiple tokens in the lexicon at the same time, and return them #
########################################################################################

def lookup_multiple_readings(tokens):
	# Create an empty list to hold the readings
	readings = []
	# For each of the input tokens...
	for token in tokens:
		# If the token is in the lexicon (of if the lower-cased version of the token is in the lexicon), format each entry of the token found in the lexicon and add it to the list of readings
		if token in corcencc_lexicon:
			readings = readings + [[token, [x["pos_enriched"]], x["lemma"], [x["lemma_en"]], ""] for x in corcencc_lexicon[token]]
		elif token.lower() in corcencc_lexicon:
			readings = readings + [[token.lower(), [x["pos_enriched"]], x["lemma"], [x["lemma_en"]], ""] for x in corcencc_lexicon[token.lower()]]
		# Find a list of possible mutations for the input token
		possible_mutations = lookup_mutation(token) # NOTE - It looks like this needs finishing, nothing appears to be done with the list of possible mutations...
	# Return the list of readings
	return readings

################################################################################################
# For a given (rich) POS tag, split it into a list of its morphological elements and return it #
################################################################################################

def tag_morphology(tag):
	# Create an empty list to hold the morphological elements of the input POS tag
	morphology = []
	# If the input POS tag is in the morphological table, find it's location in the table and return the appropriate list of its morphological elements
	if tag in [x[0] for x in morphological_table]:
		location = [x[0] for x in morphological_table].index(tag)
		morphology = morphological_table[location][1]
	# Otherwise (input POS tag is not in the morphological table), return add the input POS tag to the morphology list
	else:
		morphology = [tag]
	# Return the list of morphological elements of the input POS tag
	return morphology

##############################################################################################################################
# For a given token, assume every possible mutation that could have been applied to it and return a list its unmutated forms #
##############################################################################################################################

def lookup_mutation(input_token):
	# Lower-case the input token and create an empty list to hold the unmutated forms of the input token.
	token = input_token.lower()
	unmutated = []
	# For every common Welsh mutation, id the token starts with a mutated beginning replace it with the standard beginning it is derived from, and append a tuple of the unmutated word and the type of mutation (am, nm, sm or hm) to the unmutated list
	if token[:2] == "ch":
		unmutated.append(("c{}".format(token[2:]), "am"))
	if token[:2] == "ph":
		unmutated.append(("p{}".format(token[2:]), "am"))
	if token[:2] == "th":
		unmutated.append(("t{}".format(token[2:]), "am"))
	if token[:3] == "ngh":
		unmutated.append(("c{}".format(token[3:]), "nm"))
	if token[:2] == "mh":
		unmutated.append(("p{}".format(token[2:]), "nm"))
	if token[:2] == "nh":
		unmutated.append(("t{}".format(token[2:]), "nm"))
	if token[:2] == "ng":
		unmutated.append(("g{}".format(token[2:]), "nm"))
	if token[:1] == "m":
		unmutated.append(("b{}".format(token[1:]), "nm"))
	if token[:1] == "n":
		unmutated.append(("d{}".format(token[1:]), "nm"))
	if token[:1] == "g":
		unmutated.append(("c{}".format(token[1:]), "sm"))
	if token[:1] == "b":
		unmutated.append(("p{}".format(token[1:]), "sm"))
	if token[:1] == "d":
		unmutated.append(("t{}".format(token[1:]), "sm"))
	if token[:1] == "f":
		unmutated.append(("b{}".format(token[1:]), "sm"))
		unmutated.append(("m{}".format(token[1:]), "sm"))
	if token[:1] == "l":
		unmutated.append(("ll{}".format(token[1:]), "sm"))
	if token[:1] == "r":
		unmutated.append(("rh{}".format(token[1:]), "sm"))
	if token[:2] == "dd":
		unmutated.append(("d{}".format(token[2:]), "sm"))
	if token[:2] == "ha":
		unmutated.append(("a{}".format(token[2:]), "hm"))
	if token[:2] == "he":
		unmutated.append(("e{}".format(token[2:]), "hm"))
	if token[:2] == "hi":
		unmutated.append(("i{}".format(token[2:]), "hm"))
	if token[:2] == "ho":
		unmutated.append(("o{}".format(token[2:]), "hm"))
	if token[:2] == "hu":
		unmutated.append(("u{}".format(token[2:]), "hm"))
	if token[:2] == "hw":
		unmutated.append(("w{}".format(token[2:]), "hm"))
	if token[:2] == "hy" and token != "hyn":
		unmutated.append(("y{}".format(token[2:]), "hm"))
	unmutated.append(("g{}".format(token), "sm"))
	# If the input token was originally upper case, create a duplicate list of every entry in the unmutated list, except with a capital letter at the start of each entry, and add the two lists together
	if input_token[0].isupper():
		capitals = []
		for mutation in unmutated:
			capitals.append(("{}{}".format(mutation[0][:1].upper(), mutation[0][1:]), mutation[1]))
		unmutated = unmutated + capitals
	# Return the list of unmutated tokens
	return unmutated

####################################################################################################
# Format a list of English lemmas as a string can be included as part of a single Welsh CG reading #
####################################################################################################

def format_en_lemmas(lemmas):
	# Create a variable to hold a string to hold all of the formatted English lemmas, and a list to hold the individually formatted English lemmas
	en_lemma_string = ""
	formatted_lemmas = []
	# Format each input lemma and append it to the list of individually formatted lemmas
	for lemma in lemmas:
		formatted_lemmas.append(":{}:".format(lemma))
	# Join the list of individually formatted lemmas as a string (separated by a space) and return it
	en_lemma_string = " ".join(formatted_lemmas)
	return en_lemma_string

def pos_tag(token_count, tokenised_files, output_location):
	# Create an empty list to hold the POS tagged tokens
	tagged_tokens = []
	# Create variables to store the total numbers of sentences and tokens
	total_sentences, total_tokens = 0, 0
	# Create a variable to store the CG-formatted token readings
	cg_readings = ""
	# Create variables to record the number of untagged tokens, the number of tokens with readings, the number of tokens without readings, and the number of tokens which have been assumed to be proper nouns
	untagged_tokens, with_readings, without_readings, guessed_pns = 0, 0, 0, 0
	# If information about where to print to was given, create a bar to show the progress of finding token readings
	readings_bar = None
	if len(output_location) > 0:
		readings_bar = Bar("Finding token readings", max=token_count)
	# For each tokenised file passed to the pos_tag function...
	for file_id, file in enumerate(tokenised_files):
		# For each segment in this file...
		for segment_id, segment in enumerate(file[2]):
			# For each sentence in this segment...
			for sentence_id, sentence in enumerate(segment[1]):
				# Make sure there are no empty tokens in the sentence
				tokens = list(filter(None, sentence[1]))
				# For each token...
				for token_id, token in enumerate(tokens):
					# If the progress bar for finding token readings was created, increment it
					if readings_bar != None:
						readings_bar.next()
					# Create an empty list to hold the CG readings for the token
					readings = []
					# Find out if this token can be assigned a definite (unambigous) tag
					pos = find_definite_tags(token[0])
					# If the returned pos tag was a punctuation mark, a symbol, a digit, an acronym, or an abbreviation...
					if pos != "" and (pos[:pos.index(":")] == "Atd" or pos[pos.index(":")+1:] in ["Gwsym", "Gwdig", "Gwacr", "Gwtalf"]):
						# Append the appropriate details to the list of readings
						readings.append([token[0], " ".join(tag_morphology(pos[pos.index(":")+1:])), token[0], [token[0]], ""])
						# Print the appropriate details to the CG-formatted token readings
						cg_readings += "\"<{}>\"\n\t\"{}\" {{{}}} [cy] {} :{}:\n".format(token[0], token[0], token[1]["position"], " ".join(tag_morphology(pos[pos.index(":")+1:])), token[0])
						# Increment the number of tokens with readings by one
						with_readings += 1
					# Otherwise...
					else:
						# Print the token itself to the CG-formatted token readings
						cg_readings += "\"<{}>\"\n".format(token[0])
						# Look up potential readings for this token
						readings = lookup_readings(token[0])
						# If no readings were returned...
						if len(readings) == 0:
							# If the first letter of the reading is uppercase...
							if token[0][0].isupper():
								# Print the appropriate details for a masculine and a feminine proper noun to the CG-formatted token readings
								cg_readings += "\t\"{}\" {{{}}} [cy] {} :{}:\n".format(token[0], token[1]["position"], "E p g", token[0])
								cg_readings += "\t\"{}\" {{{}}} [cy] {} :{}:\n".format(token[0], token[1]["position"], "E p b", token[0])
								# Increment the number of tokens with readings and the number of tokens which have been assumed to be proper nouns by 1
								with_readings += 1
								guessed_pns += 1
							# If the token is in the list of pre-existing list of contractions and prefixes...
							elif token[0] in contractions_and_prefixes.keys():
								# If the token is a contraction, look up all of it's possible full forms
								if contractions_and_prefixes[token[0]][0] == "contraction":
									readings = lookup_multiple_readings(contractions_and_prefixes[token[0]][1])						
									# If the returned readings were not empty...
									if len(readings) > 0:
										# For each reading...
										for reading in readings:
											# Record the English lemmas for each reading and split its rich tag into its morphological parts
											en_lemmas = format_en_lemmas(reading[3])
											morphology = tag_morphology(reading[1][0])
											# If splitting the tag returned one or more morphological parts, convert the parts to a string in which they are separated by a space
											tags = " ".join(tag_morphology(reading[1][0]))
											# Print the appropriate details for the reading to the CG-formatted token readings
											cg_readings += "\t\"{}\" {{{}}} [cy] {} {}\n".format(reading[2], token[1]["position"], tags, en_lemmas)
										# Increment the number of tokens with readings by one
										with_readings += 1
									# Otherwise...
									else:
										# Print a reading of 'unk' to the CG-formatted token readings
										cg_readings += "\t\"{}\" {{{}}} {}\n".format(token[0], token[1]["position"], "unk")
										# Increment the number of tokens without readings by one
										without_readings += 1
							# If the token ends with an apostrophe...
							elif token[0][-1:] == "'":
								# Look up all possible readings for that token with the apostrophe replaced by an 'f', an 'r', or an 'l'
								readings = lookup_multiple_readings(["{}f".format(token[0][:-1]), "{}r".format(token[0][:-1]), "{}l".format(token[0][:-1])])
								if len(readings) > 0:
									# For each reading...
									for reading in readings:
										# Record the English lemmas for each reading and split its rich tag into its morphological parts
										en_lemmas = format_en_lemmas(reading[3])
										morphology = tag_morphology(reading[1][0])
										# If splitting the tag returned one or more morphological parts, convert the parts to a string in which they are separated by a space
										tags = " ".join(tag_morphology(reading[1][0]))
										# Print the appropriate details for the reading to the CG-formatted token readings
										cg_readings += "\t\"{}\" {{{},{}}} [cy] {} {}\n".format(reading[2], total_sentences + sentence_id + 1, token_id + 1, tags, en_lemmas)
									# Increment the number of tokens with readings by one
									with_readings += 1
								else:
									# Print a reading of 'unk' to the CG-formatted token readings
									cg_readings += "\t\"{}\" {{{},{}}} {}\n".format(token[0], total_sentences + sentence_id + 1, token_id + 1, "unk")
									# Increment the number of tokens without readings by one
									without_readings += 1
							# If the token ends with a vowel...
							elif token[0][-1:] == ["a", "â", "e", "ê", "i", "î", "o", "ô", "u", "û", "w", "ŵ", "y", "ŷ"]:
								# Look up all possible readings for that token with the apostrophe replaced by an 'f'
								readings = lookup_multiple_readings(["{}f".format(token[0])])
								# If the returned readings were not empty...
								if len(readings) > 0:
									# For each reading...
									for reading in readings:
										# Record the English lemmas for each reading and split its rich tag into its morphological parts
										en_lemmas = format_en_lemmas(reading[3])
										morphology = tag_morphology(reading[1][0])
										# If splitting the tag returned one or more morphological parts, convert the parts to a string in which they are separated by a space
										tags = " ".join(tag_morphology(reading[1][0]))
										# Print the appropriate details for the reading to the CG-formatted token readings
										cg_readings += "\t\"{}\" {{{},{}}} [cy] {} {}\n".format(reading[2], total_sentences + sentence_id + 1, token_id + 1, tags, en_lemmas)
									# Increment the number of tokens with readings by one
									with_readings += 1
								else:
									# Print a reading of 'unk' to the CG-formatted token readings
									cg_readings += "\t\"{}\" {{{},{}}} {}\n".format(token[0], total_sentences + sentence_id + 1, token_id + 1, "unk")
									# Increment the number of tokens without readings by one
									without_readings += 1
							# If the token ends with a consonant...
							elif token[0][-1:] == ["b", "c", "d", "f", "g", "h", "j", "l", "m", "n", "p", "r", "s", "t"] or token[0][-2:] == ["ch", "dd", "ff", "ng", "ll", "ph", "rh", "th"]:
								# Look up all possible readings for that token with the apostrophe replaced by an 'r' or an 'l'
								readings = lookup_multiple_readings(["{}r".format(token[0]), "{}l".format(token[0])])
								# If the returned readings were not empty...
								if len(readings) > 0:
									# For each reading...
									for reading in readings:
										# Record the English lemmas for each reading and split its rich tag into its morphological parts
										en_lemmas = format_en_lemmas(reading[3])
										morphology = tag_morphology(reading[1][0])
										# If splitting the tag returned one or more morphological parts, convert the parts to a string in which they are separated by a space
										tags = " ".join(tag_morphology(reading[1][0]))
										# Print the appropriate details for the reading to the CG-formatted token readings
										cg_readings += "\t\"{}\" {{{},{}}} [cy] {} {}\n".format(reading[2], total_sentences + sentence_id + 1, token_id + 1, tags, en_lemmas)
									# Increment the number of tokens with readings by one
									with_readings += 1
								else:
									# Print a reading of 'unk' to the CG-formatted token readings
									cg_readings += "\t\"{}\" {{{},{}}} {}\n".format(token[0], total_sentences + sentence_id + 1, token_id + 1, "unk")
									# Increment the number of tokens without readings by one
									without_readings += 1
							# Otherwise...
							else:
								# Print a reading of 'unk' to the CG-formatted token readings
								cg_readings += "\t\"{}\" {{{},{}}} {}\n".format(token[0], total_sentences + sentence_id + 1, token_id + 1, "unk")
								# Increment the number of tokens without readings by one
								without_readings += 1
						# Otherwise, if readings were returned...
						else:
							# Create an empty list to hold the indexes of the readings that should be removed
							to_remove = []
							# For each of the token's readings...
							for reading_id, reading in enumerate(readings):
								# If:
								##### it is not the first reading
								# AND the reading's token is the same as the token of the previous reading
								# AND the reading's POS tag is the same as the POS tag of the previous reading
								# AND the reading's lemma is the same as the lemma of the previous reading
								# AND the reading's English lemma is not the same as the English lemma of the previous reading
								if reading_id > 0 and (reading[0].lower() == readings[reading_id-1][0].lower()) and (reading[1] == readings[reading_id-1][1]) and (reading[2] == readings[reading_id-1][2]) and (reading[3] != readings[reading_id-1][3]):
									# Append the reading's English lemma to the English lemma of the previous reading and add the index of the current reading to the 'to_remove' list
									readings[reading_id-1][3].append(reading[3][0])
									to_remove.append(reading_id)
							# Reverse the 'to_remove' list and if it isn't empty, work backward through the readings for the current token deleting the appropriate ones
							to_remove.reverse()
							if len(to_remove) > 0:
								for index in to_remove:
									del readings[index]
							# For each remaining reading...
							for reading in readings:
								# Record the English lemmas and create a string based on the (morphological elements of the) POS tag 
								en_lemmas = format_en_lemmas(reading[3])
								tags = " ".join(reading[1][0])# if len(reading[1][0]) > 1 else reading[1][0]
								# Create a variable for the mutation description and if the mutation section of the reading is not empty, format the mutation description accordingly
								mutation_desc = " + {}".format(reading[4]) if reading[4] != "" else ""
								# Print the appropriate details for the reading to the CG-formatted token readings
								cg_readings += "\t\"{}\" {{{},{}}} [cy] {} {}{}\n".format(reading[2], total_sentences + sentence_id + 1, token_id + 1, tags, en_lemmas, mutation_desc)
							# Increment the number of tokens with readings by one
							with_readings += 1	
					# Append the appropriate details about this token to the list of POS tagged tokens
					tagged_tokens.append([token[0], token[1]["location"], token[1]["position"]])
					#tagged_tokens.append([token[0], [file_id, segment_id, sentence_id], "{},{}".format(total_sentences + sentence_id + 1, token_id + 1)])
				# Append a newline to the CG-formatted readings
				cg_readings += "\n"
				# Increment the total number of tokens by the number of tokens in the current sentence
				total_tokens += sentence[0]
			# Increment the total number of sentences by the number of sentences in the current segment
			total_sentences += segment[0]
	# If output details are being printed and the progress bar for finding token readings was created...
	if len(output_location) > 0 and readings_bar != None:
		# Finish the progress bar for finding token readings
		readings_bar.finish()
		# Print output data about the readings produced and the number of words assumed to be proper nouns to the terminal
		print("From {} tokens:\n--- {} tokens were given readings\n--- {} tokens without readings were assumed to be proper nouns\n--- {} tokens are still without readings (marked as 'unknown')".format(token_count, str(with_readings), guessed_pns, str(without_readings)))
	# If VISL CG-3 was not located...
	if vislcg3_location == None or vislcg3_location == "" or vislcg3_location == bytearray():
		# Print a warning that VISL CG-3 is not installed, and return that it is missing
		print("\nERROR: VISL CG-3 could not be found, and is required to continue using CyTag. Please follow the instructions in the README file to install it\n")
		return("vislcg3 missing")
	# Otherwise...
	else:
		# If output details are being printed, print that CG-3 is being run
		if len(output_location) > 0:
			print("\nRunning CG-3\n")
		# Run VISL CG-3 in order to get its output
		cg_output = run_cg(cg_readings, vislcg3_location)
		# If running CG-3 did not return CG-formatted output readings...
		if cg_output == "":
			# Print a warning that VISL CG-3 returned an empty output, and return that it was empty
			print("\nVISL CG-3 ERROR: An empty output was returned from CG-3. If details of an error were printed above this message, please try and resolve them. Otherwise, contact us via the details in the README file\n")
			return("vislcg3 empty")
		# Or, if running CG-3 returned something other than CG-formatted output readings...
		elif cg_output.splitlines()[0].startswith("\"<") == False and cg_output.splitlines()[0].endswith(">\"") == False:
			# Print a warning that the VISL CG-3 output was not CG-formatted readings, and return that there was an error
			print("VISL CG-3 ERROR: The returned output was not CG-formatted readings ---\n{}".format(cg_output))
			return("vislcg3 error")
		# Otherwise...
		else:
			# If output details are being printed...
			if len(output_location) > 0:
				# Print the CG-formatted readings and the output from running CG-3 to output files
				print(cg_readings, file=open("{}/../{}/{}/{}_readings".format(os.path.dirname(os.path.abspath(__file__)), "outputs", output_location[0], output_location[1]), "w"))
				print(cg_output, file=open("{}/../{}/{}/{}_readingsPostCG".format(os.path.dirname(os.path.abspath(__file__)), "outputs", output_location[0], output_location[1]), "w"))
			# If the gazetteers were not already loaded, load them now
			if bool(gazetteers) == False:
				load_gazetteers()
			# If output details are being printed...
			if len(output_location) > 0:
				# Create empty lists to store existing and new unknown words
				existing_unknown_words = []
				new_unknown_words = []
				# If the unknown words file already exists, load its contents into the list of existing unknown words
				if os.path.exists("{}/../{}/unknown_words".format(os.path.dirname(os.path.abspath(__file__)), "outputs")):
					with open("{}/../{}/unknown_words".format(os.path.dirname(os.path.abspath(__file__)), "outputs")) as loaded_unknowns:
						existing_unknown_words = loaded_unknowns.read().splitlines()
			# Create an empty list to store the readings and variables for the total number of readings
			cg_readings = []
			cg_readingcount = 0
			# Create variables for the numbers of tokens that had one reading, had multiple readings, or were unknown post-CG
			one_reading, multiple_readings, unknown = 0, 0, 0
			# Create variables for the number of unknown tokens found in the gazetteers, and the number of ambiguous tokens found in the gazetteers
			unknown_gazetteer, ambiguous_gazetteer = 0, 0
			# Create variables for the number of tokens assumed to be gender ambiguous (masculine of feminine) proper nounts, the number of tokens with multiple readings of the same POS tag, and the number of tokens found using the coverage dictionaries
			neutral_pns, same_tag, in_coverage = 0, 0, 0
			# Create a variable for the number of tokens that are still ambiguous
			still_ambiguous = 0
			# Create variables for the numbers of disambiguated tokens and undisambiguated (ambiguous) tokens
			disambiguated, undisambiguated = 0, 0
			# For each non-empty line the post-CG readings output...
			for i, line in enumerate(cg_output.splitlines()):
				# IF the line is not empty...
				if line != "":
					# If the line doesn't start with a tab, append a new list containing the line to the readings list and increment the total number of readings by one
					if line[:1] != "\t":
						cg_readings.append([line])
						cg_readingcount += 1
					# Otherwise (if the line does start with a tab), append the line to the previous list in the readings list
					else:
						cg_readings[cg_readingcount-1].append(line)
			# If information about where to print to was given, create a bar to show the progress of mapping CG-3 output to tokens
			cgmapping_bar = None
			if len(output_location) > 0:
				cgmapping_bar = Bar("Mapping CG-3 output to tokens", max=len(tagged_tokens))
			# For each POS tagged token...
			for i, token in enumerate(tagged_tokens):
				# If the progress bar for mapping CG-3 output to tokens was created, increment it
				if cgmapping_bar != None:
					cgmapping_bar.next()
				# Create variables for the lemma, basic and rich POS tags, and mutation details
				lemma, basic_pos, rich_pos, mutation = "", "", "", ""
				# If the token has two corresponding CG readings...
				if len(cg_readings[i]) == 2:
					# If the readings are not 'unknown'...
					if cg_readings[i][1][-3:] != "unk":
						# Find the token as it is printed in the reading
						reading_token = cg_readings[i][0][2:-2]
						# Mark cutoff points in the reading string for the lemma, position, POS tag and mutation details
						lemma_cutoff = cg_readings[i][1].find("\" {")
						position_cutoff = cg_readings[i][1].find("} [")
						tag_cutoff = cg_readings[i][1].find(" :")
						mutation_startcutoff = cg_readings[i][1].find(": + ")
						# Using the previously defined cutoff points, slice the reading string to extract the lemma, position, and POS tag for the reading
						lemma = cg_readings[i][1][2:lemma_cutoff]
						position = cg_readings[i][1][lemma_cutoff+3:position_cutoff]
						pos_tag = cg_readings[i][1][position_cutoff+7:tag_cutoff]
						# If the token and its position are the same as they are printed in the reading...
						if token[0] == reading_token and token[2] == position:
							# Append the lemma extracted from the reading to the token
							token.append(lemma)
							# Using the tag categories dictionary, use the POS tag extracted from the reading to find the corresponding basic POS tag, and append it to the token
							token.append([x[0] for x in tag_categories if pos_tag.replace(" ", "") in x[1]][0] if len([x[0] for x in tag_categories if pos_tag.replace(" ", "") in x[1]]) > 0 else pos_tag.replace(" ", ""))
							# Append the POS tag extracted from the reading (without spaces) to the token
							token.append(pos_tag.replace(" ", ""))
							# If a mutation details cutoff point was found in the reading, slice the mutation details from the reading and append them to the token
							if mutation_startcutoff != -1:
								token.append(cg_readings[i][1][mutation_startcutoff+4:])
						# Increment the number of disambiguated tokens by one
						disambiguated += 1
						# Increment the number of tokens with one reading post-CG by one
						one_reading += 1
					# Otherwise (the reading is 'unknown')...
					else:
						# Mark cutoff points in the reading string for the lemma and position
						lemma_cutoff = cg_readings[i][1].find("\" {")
						position_cutoff = cg_readings[i][1].find("} unk")
						# Using the previously defined cutoff points, slice the reading string to extract the lemma and position for the reading
						lemma = cg_readings[i][1][2:lemma_cutoff]
						position = cg_readings[i][1][lemma_cutoff+3:position_cutoff]
						# Append the lemma extracted from the reading to the token
						token.append(lemma)
						# If the token is in one of the gazetteers, append the appropriate POS tags to the token
						if token[0] in gazetteers["givennames_m"] or token[0] in gazetteers["givennames_f"] or token[0] in gazetteers["surnames"] or token[0] in gazetteers["places"]:
							token.append("E")
							if token[0] in gazetteers["givennames_m"] and token[0] not in gazetteers["givennames_f"]:
								token.append("Epg")
							elif token[0] in gazetteers["givennames_f"] and token[0] not in gazetteers["givennames_m"] and len(token) == 5:
								token.append("Epb")
							elif token[0] in gazetteers["givennames_f"] and token[0] in gazetteers["givennames_m"] and len(token) == 5:
								token.append("Ep")
							elif token[0] in gazetteers["surnames"] or token[0] in gazetteers["places"] and len(token) == 5:
								token.append("Ep")
							# Increment the number of tokens that were unknown but found in the gazetteer by one
							unknown_gazetteer += 1
							# Increment the number of disambiguated tokens by one
							disambiguated += 1
						# Otherwise... set the basic and rich POS tags to 'unk'
						else:
							# Append 'unk' to the token twice (as both the basic and rich POS tags)
							token.append("unk")
							token.append("unk")
							# If output details are being printed...
							if len(output_location) > 0:
								# Add the token to the list of unknown words
								new_unknown_words.append(token[0])
							# Increment the number of undisambiguated tokens by one
							undisambiguated += 1
						# Increment the number of unknown tokens post-CG by one
						unknown += 1
				# Otherwise (the number of corresponsing CG readings for the token is NOT 2)... 
				else:
					# Increment the number of tokens with multiple readings post-CG by one
					multiple_readings += 1
					# Find the remaining ambiguous readings for the token in question
					ambiguous_readings = cg_readings[i][1:]
					# If there are 2 ambiguous readings remaining...
					if len(ambiguous_readings) == 2:	
						# Extract the POS tags for each of the two readings
						pos_tag1 = ambiguous_readings[0][ambiguous_readings[0].find("} [")+7:ambiguous_readings[0].find(" :")]
						pos_tag2 = ambiguous_readings[1][ambiguous_readings[1].find("} [")+7:ambiguous_readings[1].find(" :")]
						# If the 2 ambiguous readings are a feminine proper noun and a masculine proper noun...
						if "E p g" in [pos_tag1, pos_tag2] and "E p b" in [pos_tag1, pos_tag2]:
							# Find the token for (one of) the reading(s) 
							reading_token = cg_readings[i][0][2:-2]
							# Mark cutoff points in (one of) the reading string(s) for the lemma, position and POS tag
							lemma_cutoff = ambiguous_readings[0].find("\" {")
							position_cutoff = ambiguous_readings[0].find("} [")
							tag_cutoff = ambiguous_readings[0].find(" :")
							# Using the previously defined cutoff points, slice the reading string to extract the lemma, position and POS tag for the reading
							lemma = ambiguous_readings[0][2:lemma_cutoff]
							position = ambiguous_readings[0][lemma_cutoff+3:position_cutoff]
							pos_tag = ambiguous_readings[0][position_cutoff+7:tag_cutoff]
							# If the token and its position are the same as they are printed in the reading...
							if token[0] == reading_token and token[2] == position:
								# Append the lemma extracted from the reading to the token
								token.append(lemma)
								# If the token is in one of the gazetteers, append the appropriate POS tags to the token
								if token[0] in gazetteers["givennames_m"] or token[0] in gazetteers["givennames_f"] or token[0] in gazetteers["surnames"] or token[0] in gazetteers["places"]:
									token.append("E")
									if token[0] in gazetteers["givennames_m"] and token[0] not in gazetteers["givennames_f"]:
										token.append("Epg")
									elif token[0] in gazetteers["givennames_f"] and token[0] not in gazetteers["givennames_m"] and len(token) == 5:
										token.append("Epb")
									elif token[0] in gazetteers["givennames_f"] and token[0] in gazetteers["givennames_m"] and len(token) == 5:
										token.append("Ep")
									elif token[0] in gazetteers["surnames"] or token[0] in gazetteers["places"] and len(token) == 5:
										token.append("Ep")
									# Increment the number of tokens that were ambiguous but found in the gazetteer by one
									ambiguous_gazetteer += 1
									# Increment the number of disambiguated tokens by one
									disambiguated += 1
								# Otherwise (the token is not in one of the gazetteers)...
								else:
									# Append the appropriate POS tags to the token such that it is a proper noun of no specified gender
									token.append("E")
									token.append("Ep")
									# Increment the number of tokens that are classed as proper nouns with undiscernible gender by one
									neutral_pns += 1
									# Increment the number of disambiguated tokens by one
									disambiguated += 1
						# Or, if both POS tags are the same (but are NOT feminine proper noun and masculine proper noun)...
						elif pos_tag1 == pos_tag2:
							# Find the token for (one of) the reading(s) 
							reading_token = cg_readings[i][0][2:-2]
							# Mark cutoff points in (one of) the reading string(s) for the lemma, position and POS tag
							lemma_cutoff = cg_readings[i][1].find("\" {")
							position_cutoff = cg_readings[i][1].find("} [")
							tag_cutoff = cg_readings[i][1].find(" :")
							# Using the previously defined cutoff points, slice the reading string to extract the lemma, position and POS tag for the reading
							lemma = cg_readings[i][1][2:lemma_cutoff]
							position = cg_readings[i][1][lemma_cutoff+3:position_cutoff]
							pos_tag = cg_readings[i][1][position_cutoff+7:tag_cutoff]
							# If the token and its position are the same as they are printed in the reading...
							if token[0] == reading_token and token[2] == position:
								# Append the lemma extracted from the reading to the token
								token.append(lemma)
								# Using the tag categories dictionary, use the POS tag extracted from the reading to find the corresponding basic POS tag, and append it to the token
								token.append([x[0] for x in tag_categories if pos_tag.replace(" ", "") in x[1]][0] if len([x[0] for x in tag_categories if pos_tag.replace(" ", "") in x[1]]) > 0 else pos_tag.replace(" ", ""))
								# Append the POS tag extracted from the reading (without spaces) to the token
								token.append(pos_tag.replace(" ", ""))
							# Increment the number of tokens that have more than one reading with the same POS tag by one
							same_tag += 1
							# Increment the number of disambiguated tokens by one
							disambiguated += 1
						# Otherwise (the 2 ambiguous readings are NOT the same and are NOT feminine proper noun and masculine proper noun)...
						else:
							# If the 'check_coverage' switch is set to True...
							if check_coverage == True:
								# If the token is in the cy_coverage dictionary...
								if token[0] in cy_coverage.keys():
									# Find the token for (one of) the reading(s) 
									reading_token = cg_readings[i][0][2:-2]
									# Mark cutoff points in one of the reading string for the lemma and position
									lemma_cutoff = ambiguous_readings[0].find("\" {")
									position_cutoff = ambiguous_readings[0].find("} [")
									# Using the previously defined cutoff points, slice the reading string to extract the lemma and position for the reading
									lemma = ambiguous_readings[0][2:lemma_cutoff]
									position = ambiguous_readings[0][lemma_cutoff+3:position_cutoff]
									# If the token and its position are the same as they are printed in the reading...
									if token[0] == reading_token and token[2] == position:
										# Append the lemma extracted from the reading to the token
										token.append(lemma)
										# Find the most likely tags for the token from the cy_coverage dictionary, and append them to the token
										tags = cy_coverage[token[0]].split(":")
										token.append(tags[0])
										token.append(tags[1])
									# Increment the number of tokens found in the coverage dictionaries by one
									in_coverage += 1
									# Increment the number of disambiguated tokens by one
									disambiguated += 1
								# If the lower-cased token is in the cy_coverage dictionary...
								elif token[0].lower() in cy_coverage.keys():
									# Find the token for (one of) the reading(s) 
									reading_token = cg_readings[i][0][2:-2]
									# Mark cutoff points in one of the reading string for the lemma and position
									lemma_cutoff = ambiguous_readings[0].find("\" {")
									position_cutoff = ambiguous_readings[0].find("} [")
									# Using the previously defined cutoff points, slice the reading string to extract the lemma and position for the reading
									lemma = ambiguous_readings[0][2:lemma_cutoff]
									position = ambiguous_readings[0][lemma_cutoff+3:position_cutoff]
									# If the lower-cased token and its position are the same as they are printed in the reading...
									if token[0].lower() == reading_token and token[2] == position:
										# Append the lemma extracted from the reading to the token
										token.append(lemma)
										# Find the most likely tags for the lower-cased token from the cy_coverage dictionary, and append them to the token
										tags = cy_coverage[token[0].lower()].split(":")
										token.append(tags[0])
										token.append(tags[1])
									# Increment the number of tokens found in the coverage dictionaries by one
									in_coverage += 1
									# Increment the number of disambiguated tokens by one
									disambiguated += 1
								# Otherwise...
								else:
									# Increment the number of ambiguous tokens post-CG that are still ambiguous by one
									still_ambiguous += 1
									# Increment the number of undisambiguated tokens by one
									undisambiguated += 1
							# Otherwise (the 'check_coverage' switch is set to False)...
							else:
								# Increment the number of ambiguous tokens post-CG that are still ambiguous by one
								still_ambiguous += 1
								# Increment the number of undisambiguated tokens by one
								undisambiguated += 1
					# Otherwise (the number of ambiguous readings remaining is NOT 2)...
					else:
						# If the token is in one of the gazetteers...
						if token[0] in gazetteers["givennames_m"] or token[0] in gazetteers["givennames_f"] or token[0] in gazetteers["surnames"] or token[0] in gazetteers["places"]:
							# Append the token itself to the token as its own lemma
							token.append(token[0])
							# Append the appropriate POS tags to the token
							token.append("E")
							if token[0] in gazetteers["givennames_m"] and token[0] not in gazetteers["givennames_f"]:
								token.append("Epg")
							elif token[0] in gazetteers["givennames_f"] and token[0] not in gazetteers["givennames_m"] and len(token) == 5:
								token.append("Epb")
							elif token[0] in gazetteers["givennames_f"] and token[0] in gazetteers["givennames_m"] and len(token) == 5:
								token.append("Ep")
							elif token[0] in gazetteers["surnames"] or token[0] in gazetteers["places"] and len(token) == 5:
								token.append("Ep")
							# Increment the number of ambiguous tokens found in the gazetteers by one
							ambiguous_gazetteer += 1
							# Increment the number of disambiguated tokens by one
							disambiguated += 1
						# Otherwise...
						else:
							# If the 'check_coverage' switch is set to True...
							if check_coverage == True:
								# If the token is in the cy_coverage dictionary...
								if token[0] in cy_coverage.keys():
									# Find the token for (one of) the reading(s) 
									reading_token = cg_readings[i][0][2:-2]
									# Mark cutoff points in one of the reading string for the lemma and position
									lemma_cutoff = ambiguous_readings[0].find("\" {")
									position_cutoff = ambiguous_readings[0].find("} [")
									# Using the previously defined cutoff points, slice the reading string to extract the lemma, position and POS tag for the reading
									lemma = ambiguous_readings[0][2:lemma_cutoff]
									position = ambiguous_readings[0][lemma_cutoff+3:position_cutoff]
									# If the token and its position are the same as they are printed in the reading...
									if token[0] == reading_token and token[2] == position:
										# Append the lemma extracted from the reading to the token
										token.append(lemma)
										# Find the most likely tags for the token from the cy_coverage dictionary, and append them to the token
										tags = cy_coverage[token[0]].split(":")
										token.append(tags[0])
										token.append(tags[1])
									# Increment the number of tokens found in the coverage dictionaries by one
									in_coverage += 1
									# Increment the number of disambiguated tokens by one
									disambiguated += 1
								# If the lower-cased token is in the cy_coverage dictionary...
								elif token[0].lower() in cy_coverage.keys():
									# Find the token for (one of) the reading(s) 
									reading_token = cg_readings[i][0][2:-2]
									# Mark cutoff points in one of the reading string for the lemma and position
									lemma_cutoff = ambiguous_readings[0].find("\" {")
									position_cutoff = ambiguous_readings[0].find("} [")
									# Using the previously defined cutoff points, slice the reading string to extract the lemma, position and POS tag for the reading
									lemma = ambiguous_readings[0][2:lemma_cutoff]
									position = ambiguous_readings[0][lemma_cutoff+3:position_cutoff]
									# If the lower-cased token and its position are the same as they are printed in the reading...
									if token[0].lower() == reading_token and token[2] == position:
										# Append the lemma extracted from the reading to the token
										token.append(lemma)
										# Find the most likely tags for the lower-cased token from the cy_coverage dictionary, and append them to the token
										tags = cy_coverage[token[0].lower()].split(":")
										token.append(tags[0])
										token.append(tags[1])
									# Increment the number of tokens found in the coverage dictionaries by one
									in_coverage += 1
									# Increment the number of disambiguated tokens by one
									disambiguated += 1
								else:
									# Increment the number of undisambiguated tokens by one
									undisambiguated += 1
									still_ambiguous += 1
							# Otherwise (the 'check_coverage' switch is set to False)...
							else:
								# Increment the number of undisambiguated tokens by one
								undisambiguated += 1
								still_ambiguous += 1
			# If the progress bar for mapping CG-3 output to tokens was created...
			if cgmapping_bar != None:
				# Finish the progress bar for mapping CG-3 output to tokens
				cgmapping_bar.finish()
			# If information about where to print to was given...
			if len(output_location) > 0:
				# Open an output file to store the unknown words
				unknown_output = open("{}/../{}/unknown_words".format(os.path.dirname(os.path.abspath(__file__)), "outputs"), "w")
				# Remove any duplicates from the list of new unknown words, and join them to the list of existing unknown words
				new_unknown_words = list(set(new_unknown_words))
				all_unknown_words = list(set(existing_unknown_words+new_unknown_words))
				# Write each unknown word to the output file
				for word in all_unknown_words:
					print(word, file=unknown_output)
			# If information about where to print to was given, create a bar to show the progress of the final pass over ambiguous tokens
			finalpass_bar = None
			if len(output_location) > 0:
				finalpass_bar = Bar("Final pass over ambiguous tokens", max=len(tagged_tokens))
			# For each POS tagged token...
			for i, token in enumerate(tagged_tokens):
				# If the progress bar for the final pass over ambiguous tokens was created, increment it
				if finalpass_bar != None:
					finalpass_bar.next()
				# Find the length of the sentence in which the token is found
				sentence_length = len(tokenised_files[token[1][0]][2][token[1][1]][1][token[1][2]][1])
				# Find the corresponding list of readings for the token
				token_readings = cg_readings[i]
				# Create variables for the lemma, basic_pos, and rich_pos
				lemma, basic_pos, rich_pos = "", "", ""
				# If the token does not have POS tags...
				if len(token) == 3:
					# Create a list of the possible lemmas and possible tags from the list of readings for the token
					possible_lemmas = [x[2:x.find("\" {")] for x in token_readings[1:]]
					possible_tags = [x[x.find("} [")+7:x.find(" :")].replace(" ", "") for x in token_readings[1:]]
					# Use the token itself as the lemma
					lemma = token[0]
					# If there are more than two tokens in the sentence and the 'check_coverage' switch is set to True...
					if sentence_length > 2 and check_coverage == True:
						# If this is the first token in the sentence...
						if int(token[2].split(",")[1]) == 1:
							# If the next two tokens have rich_pos tags...
							if len(tagged_tokens[i+1]) >= 5 and len(tagged_tokens[i+2]) >= 5:
								# If there is a pattern matching the rich_pos tags of the next two tokens in the tag-sequences dictionary...
								if str(["find", tagged_tokens[i+1][4], tagged_tokens[i+2][4]]) in cy_tagsequences.keys():
									# Find the rich_pos to use for the current token from the matching pattern, and use this to find the corresponding basic_pos from the tag_categories dictionary
									rich_pos = cy_tagsequences[str(["find", tagged_tokens[i+1][4], tagged_tokens[i+2][4]])]
									basic_pos = [x[0] for x in tag_categories if rich_pos in x[1]][0] if len([x[0] for x in tag_categories if rich_pos in x[1]]) > 0 else rich_pos
						# Or, if this is the last token in the sentence...
						elif int(token[2].split(",")[1]) == sentence_length:
							# If the previous two tokens have rich_pos tags...
							if len(tagged_tokens[i-2]) >= 5 and len(tagged_tokens[i-1]) >= 5:
								# If there is a pattern matching the rich_pos tags of the previous two tokens in the tag-sequences dictionary...
								if str([tagged_tokens[i-2][4], tagged_tokens[i-1][4], "find"]) in cy_tagsequences.keys():
									# Find the rich_pos to use for the current token from the matching pattern, and use this to find the corresponding basic_pos from the tag_categories dictionary
									rich_pos = cy_tagsequences[str([tagged_tokens[i-2][4], tagged_tokens[i-1][4], "find"])]
									basic_pos = [x[0] for x in tag_categories if rich_pos in x[1]][0] if len([x[0] for x in tag_categories if rich_pos in x[1]]) > 0 else rich_pos
						# Otherwise...
						else:
							# If the previous and next tokens have rich_pos tags...
							if len(tagged_tokens[i-1]) >= 5 and len(tagged_tokens[i+1]) >= 5:
								# If there is a pattern matching the rich_pos tags of the previous and next tokens in the tag-sequences dictionary...
								if str([tagged_tokens[i-1][4], "find", tagged_tokens[i+1][4]]) in cy_tagsequences.keys():
									# Find the rich_pos to use for the current token from the matching pattern, and use this to find the corresponding basic_pos from the tag_categories dictionary
									rich_pos = cy_tagsequences[str([tagged_tokens[i-1][4], "find", tagged_tokens[i+1][4]])]
									basic_pos = [x[0] for x in tag_categories if rich_pos in x[1]][0] if len([x[0] for x in tag_categories if rich_pos in x[1]]) > 0 else rich_pos
					# If the basic_pos and rich_pos variables are not empty...
					if basic_pos != "" and rich_pos != "":
						# Create an empty tag_families dictionary
						tag_families = []
						# For each possible tag, if the tag starts with the value of the basic_pos variable, append it to the tag_families dictionary
						for tag in possible_tags:
							if tag.startswith(basic_pos):
								tag_families.append(tag)
						# If the value of the rich_pos variable is one of the possible tags, use its index in the list of possible tags to find the corresponding possible lemma
						if rich_pos in possible_tags:
							lemma = possible_lemmas[possible_tags.index(rich_pos)]
						# Or, if there is only one tag in tag_families...
						elif len(tag_families) == 1:
							# Use the tag as the rich_pos, use the rich_pos to find the basic_pos from the tag_categories dictionary, and use the index of the rich_pos in the list of possible tags to find the corresponding entry from the list of possible lemmas
							rich_pos = tag_families[0]
							basic_pos = [x[0] for x in tag_categories if rich_pos in x[1]][0] if len([x[0] for x in tag_categories if rich_pos in x[1]]) > 0 else rich_pos
							lemma = possible_lemmas[possible_tags.index(rich_pos)]
						# Otherwise...
						else:
							# Join the possible lemmas together as one string and use this as the lemma variable
							lemma = " | ".join(possible_lemmas)
							# Create an empty list to hold possible basic tags
							possible_basics = []
							# For each entry in the list of possible tags, find the corresponding basic tag from the tag_categories dictionary and add this to the list of possible basic tags
							for tag in possible_tags:
								basic = [x[0] for x in tag_categories if tag in x[1]][0] if len([x[0] for x in tag_categories if tag in x[1]]) > 0 else tag
								possible_basics.append(basic)
							# Join the possible basic and rich tags together as individual strings and use these as the basic_pos and rich_pos variables
							basic_pos = " | ".join(possible_basics)
							rich_pos = " | ".join(possible_tags)
					# Otherwise...
					else:
						# Join the possible lemmas together as one string and use this as the lemma variable
						lemma = " | ".join(possible_lemmas)
						# Create an empty list to hold possible basic tags
						possible_basics = []
						# For each entry in the list of possible tags, find the corresponding basic tag from the tag_categories dictionary and add this to the list of possible basic tags
						for tag in possible_tags:
							basic = [x[0] for x in tag_categories if tag in x[1]][0] if len([x[0] for x in tag_categories if tag in x[1]]) > 0 else tag
							possible_basics.append(basic)
						# Join the possible basic and rich tags together as individual strings and use these as the basic_pos and rich_pos variables
						basic_pos = " | ".join(possible_basics)
						rich_pos = " | ".join(possible_tags)
					# Append the lemma, basic_pos and rich_pos variables to the token
					token.append(lemma)
					token.append(basic_pos)
					token.append(rich_pos)
			# If the progress bar for the final pass over ambiguous tokens was created...
			if finalpass_bar != None:
				# Finish the progress bar for the final pass over ambiguous tokens
				finalpass_bar.finish()
			# If information about where to print to was given...
			if len(output_location) > 0:
				# Print details on the numbers of disambiguated and undisambiguated tokens to the terminal
				print("\nFinal statistics from {} tokens:\n--- {} tokens disambiguated\n------ {} pruned to one reading post-CG\n------ {} ambiguous post-CG, but:\n--------- {} found to have two readings with the same POS tag\n--------- {} found to be proper nouns of ambiguous gender\n--------- {} assigned a POS tag based on the coverage dictionary\n------ {} unknown, but then found in gazetteers\n--- {} tokens undisambiguated\n------ {} still ambiguous post-CG\n------ {} unknown".format(len(tagged_tokens), disambiguated, one_reading, multiple_readings-still_ambiguous, same_tag, ambiguous_gazetteer+neutral_pns, in_coverage, unknown_gazetteer, undisambiguated, still_ambiguous, unknown))
				# Print details on the numbers of unknown words to the terminal
				print("\nUnknown words:\n--- {} unknown words recorded in 'CyTag/outputs/unknown_words'\n------ {} words in total unknown to CyTag\n".format(len(new_unknown_words), len(all_unknown_words)))
			# Return the POS tagged tokens
			return(tagged_tokens)

def run_cg(cg_readings, vislcg3_location):
	# Create a subprocess to run CG-3 using the 'cy_grammar' file
	cg_process = subprocess.Popen([vislcg3_location, '-g', '{}/../grammars/cy_grammar_2017-08-01'.format(os.path.dirname(os.path.abspath(__file__)))], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	# Run the CG-3 subprocess, using the CG-formatted readings as input
	cg_output = cg_process.communicate(input=cg_readings.encode("utf-8"))[0]
	# Return the output of the CG-3 subprocess
	return(cg_output.decode("utf-8"))

def pos_tagger(arguments, print_flag, output):
	# Check for the python libraries required by cy_postagger
	library_info = check_libraries("cy_postagger", "cy_postagger - A part-of-speech (POS) tagger for Welsh texts", ["progress", "lxml"]) if print_flag != None else None
	# If anything other than 'None' was returned from the library check, print it and then return
	if library_info != None:
		print(library_info)
		return
	# Otherwise...
	else:
		# Create an empty list to hold information about output location
		output_location = []
		# If the print flag is not 'None'...
		if print_flag != None:
			print("\ncy_postagger - A part-of-speech (POS) tagger for Welsh texts\n------------------------------------------------------------\n")
			# Set the ouptut location to the third (directory) and second (output name) arguments if a directory was given, otherwise use the second (output name) argument for both values 
			output_location = [arguments[2] if arguments[2] != None else arguments[1], arguments[1]]
			# Create any necessary output folders
			folders = create_folders(arguments)
			# If something other than 'None' was returned while trying to create ouptut folders, print it and then return
			if folders != None:
				print(folders)
				return
		# Split the input data into a tokenised output object
		output = tokeniser(arguments[0], output)
		# POS tag the tokenised output object
		tagged_tokens = pos_tag(output.total_tokens, output.files, output_location)
		# If the pos_tag function returned a list (of tagged tokens)...
		if isinstance(tagged_tokens, list):
			# Store the POS tagged tokens in the output object
			output.store_tags(tagged_tokens)
			# Return the output object
			return(output)
		# Otherwise, return
		else:
			return

if __name__ == "__main__":
	args = sys.argv[1:]
	# If there was only one argument provided and it was not a file...
	if len(args) == 1 and os.path.isfile(args[0]) != True:
		# Run the part-of-speech (POS) tagger
		pos_tagger([args[0]], None, taggedobject())
	# Otherwise:
	else:
		# Cycle through the arguments and split the input files and the text arguments into separate lists
		input_files, text_args = [], []
		for arg in args:
			input_files.append(arg) if os.path.isfile(arg) else text_args.append(arg)
		# Alert the user if there are no input files among the arguments, or if there are no text arguments
		if len(input_files) == 0 or len(text_args) == 0:
			print("ARGUMENT ERROR: One or more input files and an output filename must be specified. An optional output directory and a 'print' flag can also be specified.")
		else:
			# If more than 3 text arguments were passed, alert the user to the correct ordering and formatting for text arguments
			if len(text_args) > 3:
				print("ARGUMENT ERROR: Too many text arguments have been given. Text arguments (maximum of 3) should be: OUTPUT_FILENAME (required) OUTPUT_DIRECTORY (optional) PRINT_FLAG (optional)")
			# Otherwise...
			else:
				# Take the first text argument as output name
				output_name = text_args[0]
				# Set the output directory and print flag to 'None'
				directory, print_flag = None, None
				# If there are 3 text arguments...
				if len(text_args) == 3:
					# If the third argument is not 'print', alert the user to the coreect ordering for arguments 
					if text_args[2] != "print":
						print("ARGUMENT ERROR: '" + text_args[2] + "' is not valid for use as the print flag (which should be just 'print'). The correct order for 3 text arguments should be: OUTPUT_FILENAME OUTPUT_DIRECTORY PRINT_FLAG ('print')")
					# Otherwise...
					else:
						# Set the second text argument as the output directory and the third as the print flag 
						directory, print_flag = text_args[1], text_args[2]
						# Run the part-of-speech (POS) tagger
						pos_tagger([input_files, output_name, directory], print_flag, taggedobject())
				# Or, if there are 2 text arguments...
				elif len(text_args) == 2:
					# If the second text argument is 'print', set the print flag
					if text_args[1] == "print":
						print_flag = "print"
					# Otherwise, set the second text argument as the ouptut directory
					else:
						directory = text_args[1]
					# Run the part-of-speech (POS) tagger
					pos_tagger([input_files, output_name, directory], print_flag, taggedobject())
				# Otherwise...
				else:
					# Run the part-of-speech (POS) tagger
					pos_tagger([input_files, output_name, directory], print_flag, taggedobject())