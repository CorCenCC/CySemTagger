#!usr/bin/env python3
"""
'eurfa_extractor.py'

A script for pulling CorCenCC formatted lexicons from Kevin Donnelly's EURFA dictionary.

Accepts as arguments:
	--- The EURFA dictionary in CSV format.
	--- A name for outputting the CorCenCC formatted lexicon.

Developed at the University of Cardiff as part of the CorCenCC project (www.corcencc.org).

2016 Steve Neale <NealeS2@cardiff.ac.uk>
"""

import sys
import os
import re
import csv

def eurfa_extractor(dictionaries, lexicon_name):
	lexicon = open("{}/output_lexicons/{}".format(os.path.dirname(os.path.abspath(__file__)), lexicon_name), "w")
	extracted_entries = []
	dictionaries_used = ""
	for dictionary in dictionaries:
		dictionaries_used += "# --- {}\n".format(dictionary)
	print("# {}\n#\n# Extracted from:\n{}#\n# Created using 'eurfa_extractor.py'\n#\n#".format(lexicon_name, dictionaries_used), file=lexicon)
	for dictionary_file in dictionaries:
		print("### {} ###".format(dictionary_file), file=lexicon)
		with open(dictionary_file, newline="") as loaded_dictionary:
			dictionary = csv.reader(loaded_dictionary, delimiter=",", quotechar="\"")
			for _i, entry in enumerate(dictionary):
				entry_id = entry[0]
				if entry_id not in extracted_entries:
					pos_eurfa = ""
					gender = ""
					number = ""
					tense = ""
					extended = ""
					corcencc_tag = ""
					if len(entry) == 19:
						pos_eurfa = entry[4]#[5]
						gender = entry[5]#[6]
						number = entry[6]#[7]
						tense = entry[7]#[8]
						extended = entry[12]
						corcencc_tag = entry[13]
					elif len(entry) == 11:
						pos_eurfa = entry[5]
						gender = entry[6]
						number = entry[7]
						tense = entry[8]
					pos_basic = ["pos_b"]
					pos_enriched = ["pos_e"]
					if "adj" in pos_eurfa:
						pos_basic[0] = "Ans"					#adjective
						pos_enriched[0] = "Anscadu"			#adjective
						if gender == "f":
							pos_enriched[0] = "Anscadbu"
						if "pl" in pos_eurfa:
							pos_enriched[0] = "Anscadll"
						if "eq" in pos_eurfa:
							pos_enriched[0] = "Anscyf"
						if "comp" in pos_eurfa:
							pos_enriched[0] = "Anscym"
						if "sup" in pos_eurfa:
							pos_enriched[0] = "Anseith"
					if pos_eurfa == "adv":
						pos_basic[0] = "Adf"					# adverb
						pos_enriched[0] = "Adf"				# adverb
					if pos_eurfa == "v":
						pos_basic[0] = "B"						# verb
						#pos_enriched = "B"					# verb
						if tense == "infin":
							pos_enriched[0] = "Be"
						if "pres.indef" in tense:
							pos_enriched[0] = "Bpres3amhen"
						if "pres" in tense and "pres.indef" not in tense:
							if number == "1s":
								pos_enriched[0] = "Bpres1u"
							if number == "2s":
								pos_enriched[0] = "Bpres2u"
							if number == "3s":
								pos_enriched[0] = "Bpres3u"
							if number == "13s":
								pos_enriched = ["Bpres1u", "Bpres3u"]
							if number == "1p":
								pos_enriched[0] = "Bpres1ll"
							if number == "2p":
								pos_enriched[0] = "Bpres2ll"
							if number == "3p":
								pos_enriched[0] = "Bpres3ll"
							if number == "13p":
								pos_enriched = ["Bpres1ll", "Bpres3ll"]
							if number == "0":
								pos_enriched[0] = "Bpresamhers"
						if tense == "pres.rel":
							pos_enriched[0] = "Bpres3perth"
						if "fut" in tense:
							if number == "1s":
								pos_enriched[0] = "Bdyf1u"
							if number == "2s":
								pos_enriched[0] = "Bdyf2u"
							if number == "3s":
								pos_enriched[0] = "Bdyf3u"
							if number == "13s":
								pos_enriched = ["Bdyf1u", "Bdyf3u"]
							if number == "1p":
								pos_enriched[0] = "Bdyf1ll"
							if number == "2p":
								pos_enriched[0] = "Bdyf2ll"
							if number == "3p":
								pos_enriched[0] = "Bdyf3ll"
							if number == "13p":
								pos_enriched = ["Bdyf1ll", "Bdyf3ll"]
							if number == "0":
								pos_enriched[0] = "Bdyfamhers"
						if tense == "pluperf":
							if number == "1s":
								pos_enriched[0] = "Bgorb1u"
							if number == "2s":
								pos_enriched[0] = "Bgorb2u"
							if number == "3s":
								pos_enriched[0] = "Bgorb3u"
							if number == "13s":
								pos_enriched = ["Bgorb1u", "Bgorb3u"]
							if number == "1p":
								pos_enriched[0] = "Bgorb1ll"
							if number == "2p":
								pos_enriched[0] = "Bgorb2ll"
							if number == "3p":
								pos_enriched[0] = "Bgorb3ll"
							if number == "13p":
								pos_enriched = ["Bgorb1ll", "Bgorb3ll"]
							if number == "0":
								pos_enriched[0] = "Bgorbamhers"
						if tense == "imperf":
							if number == "1s":
								pos_enriched[0] = "Bamherff1u"
							if number == "2s":
								pos_enriched[0] = "Bamherff2u"
							if number == "3s":
								pos_enriched[0] = "Bamherff3u"
							if number == "13s":
								pos_enriched = ["Bamherff1u", "Bamherff3u"]
							if number == "1p":
								pos_enriched[0] = "Bamherff1ll"
							if number == "2p":
								pos_enriched[0] = "Bamherff2ll"
							if number == "3p":
								pos_enriched[0] = "Bamherff3ll"
							if number == "13p":
								pos_enriched = ["Bamherff1ll", "Bamherff3ll"]
							if number == "0":
								pos_enriched[0] = "Bamherffamhers"
						if tense == "past":
							if number == "1s":
								pos_enriched[0] = "Bgorff1u"
							if number == "2s":
								pos_enriched[0] = "Bgorff2u"
							if number == "3s":
								pos_enriched[0] = "Bgorff3u"
							if number == "13s":
								pos_enriched = ["Bgorff1u", "Bgorff3u"]
							if number == "1p":
								pos_enriched[0] = "Bgorff1ll"
							if number == "2p":
								pos_enriched[0] = "Bgorff2ll"
							if number == "3p":
								pos_enriched[0] = "Bgorff3ll"
							if number == "13p":
								pos_enriched = ["Bgorff1ll", "Bgorff3ll"]
							if number == "0":
								pos_enriched[0] = "Bgorffamhers"
							if number == "123sp":
								pos_enriched[0] = "Bgorffsef"
						if tense == "imper":
							if number == "1s":
								pos_enriched[0] = "Bgorch1u"
							if number == "2s":
								pos_enriched[0] = "Bgorch2u"
							if number == "3s":
								pos_enriched[0] = "Bgorch3u"
							if number == "13s":
								pos_enriched = ["Bgorch1u", "Bgorch3u"]
							if number == "1p":
								pos_enriched[0] = "Bgorch1ll"
							if number == "2p":
								pos_enriched[0] = "Bgorch2ll"
							if number == "3p":
								pos_enriched[0] = "Bgorch3ll"
							if number == "13p":
								pos_enriched = ["Bgorch1ll", "Bgorch3ll"]
							if number == "0":
								pos_enriched[0] = "Bgorchamhers"
						if tense == "subj" or tense[:5] == "subj." or tense[-4:] == ".hyp":
							if number == "1s":
								pos_enriched[0] = "Bdibdyf1u"
							if number == "2s":
								pos_enriched[0] = "Bdibdyf2u"
							if number == "3s":
								pos_enriched[0] = "Bdibdyf3u"
							if number == "13s":
								pos_enriched = ["Bdibdyf1u", "Bdibdyf3u"]
							if number == "1p":
								pos_enriched[0] = "Bdibdyf1ll"
							if number == "2p":
								pos_enriched[0] = "Bdibdyf2ll"
							if number == "3p":
								pos_enriched[0] = "Bdibdyf3ll"
							if number == "13p":
								pos_enriched = ["Bdibdyf1ll", "Bdibdyf3ll"]
							if number == "0":
								pos_enriched[0] = "Bdibdyfamhers"
						if tense == "cond":
							if number == "1s":
								pos_enriched[0] = "Bamod1u"
							if number == "2s":
								pos_enriched[0] = "Bamod2u"
							if number == "3s":
								pos_enriched[0] = "Bamod3u"
							if number == "13s":
								pos_enriched = ["Bamod1u", "Bamod3u"]
							if number == "1p":
								pos_enriched[0] = "Bamod1ll"
							if number == "2p":
								pos_enriched[0] = "Bamod2ll"
							if number == "3p":
								pos_enriched[0] = "Bamod3ll"
							if number == "13p":
								pos_enriched = ["Bamod1ll", "Bamod3ll"]
							if number == "0":
								pos_enriched[0] = "Bamodamhers"
					if pos_eurfa.startswith("prep"):
						pos_basic[0] = "Ar"					# preposition
						if entry[2] == "wedi":
							pos_basic = ["Ar", "U"]
							pos_enriched = ["Arsym", "Uberf"]
						if pos_eurfa == "prep+pron":
							if number == "1s":
								pos_enriched[0] = "Ar1u"
							if number == "2s":
								pos_enriched[0] = "Ar2u"
							if number == "3s":
								if gender == "f":
									pos_enriched[0] = "Ar3bu"
								elif gender == "m":
									pos_enriched[0] = "Ar3gu"
								else:
									pos_enriched[0] = "Ar3u"
							if number == "1p":
								pos_enriched[0] = "Ar1ll"
							if number == "2p":
								pos_enriched[0] = "Ar2ll"
							if number == "3p":
								pos_enriched[0] = "Ar3ll"
						else:
							pos_enriched[0] = "Arsym"
					if pos_eurfa.startswith("pron"):
						pos_basic[0] = "Rha"					# pronoun / determiners
						#pos_enriched = "Rha"				# pronoun / determiners
						if "rel" in pos_eurfa:
							pos_enriched[0] = "Rhaperth"
						#if number != "":
							#pos_enriched = "Rhacyff"
						#else:
						if number == "1s":
							pos_enriched[0] = "Rhapers1u" 
						if number == "2s":
							pos_enriched[0] = "Rhapers2u" 
						if number == "3s":
							if gender == "m":
								pos_enriched[0] = "Rhapers3gu" 
							if gender == "f":
								pos_enriched[0] = "Rhapers3bu" 
						if number == "1p":
							pos_enriched[0] = "Rhapers1ll" 
						if number == "2p":
							pos_enriched[0] = "Rhapers2ll" 
						if number == "3p":
							pos_enriched[0] = "Rhapers3ll" 
						if number == "sg" or number == "pl":
							pos_enriched[0] = "Rhaatb"
					if "adj.poss" in pos_eurfa:
						pos_basic[0] = "Rha"
						pos_enriched[0] = "Rhadib"
						if number == "1s":
							pos_enriched[0] = "Rhadib1u" 
						if number == "2s":
							pos_enriched[0] = "Rhadib2u" 
						if number == "3s":
							if gender == "m":
								pos_enriched[0] = "Rhadib3gu" 
							if gender == "f":
								pos_enriched[0] = "Rhadib3bu" 
						if number == "1p":
							pos_enriched[0] = "Rhadib1ll" 
						if number == "2p":
							pos_enriched[0] = "Rhadib2ll" 
						if number == "3p":
							pos_enriched[0] = "Rhadib3ll"
					if "pron.emph" in pos_eurfa:
						pos_basic[0] = "Rha"
						pos_enriched[0] = "Rhacys"
						if number == "1s":
							pos_enriched[0] = "Rhacys1u" 
						if number == "2s":
							pos_enriched[0] = "Rhacys2u" 
						if number == "3s":
							if gender == "m":
								pos_enriched[0] = "Rhacys3gu" 
							if gender == "f":
								pos_enriched[0] = "Rhacys3bu" 
						if number == "1p":
							pos_enriched[0] = "Rhacys1ll" 
						if number == "2p":
							pos_enriched[0] = "Rhacys2ll" 
						if number == "3p":
							pos_enriched[0] = "Rhacys3ll"
					if "adj.dem" in pos_eurfa:
						pos_basic[0] = "Rha"					# demonstrative
						#pos_enriched = "Rhadang"
						if gender == "" or gender == "\n":
							pos_enriched[0] = "Rhadangd"
						else:
							if gender == "m":
								pos_enriched[0] = "Rhadangg"
							if gender == "f":
								pos_enriched[0] = "Rhadangb"
						#pos_enriched = "Rhadang"			# demonstrative
					if pos_eurfa == "int":
						pos_basic[0] = "Rha"					# interrogative
						pos_enriched[0] = "Rhagof"				# interrogative
					#if pos_eurfa == "quan" or pos_eurfa == "quant":
					#	pos_basic = "Rha"					# quantifiers
					#	pos_enriched = "Rhames"				# quantifiers
					if pos_eurfa == "conj":
						pos_basic[0] = "Cys"					# conjunction
						if corcencc_tag != "" and corcencc_tag != "\\N":
							pos_enriched[0] = corcencc_tag.replace(" ", "")
						else:
							pos_enriched[0] = "Cyscyd"
					if pos_eurfa == "n":
						pos_basic[0] = "E"
						#pos_enriched = "E"
						if gender == "m":					# noun
							#pos_basic = "Eg"
							pos_enriched[0] = "Eg"
						if gender == "f":
							#pos_basic = "Eb"
							pos_enriched[0] = "Eb"
						if gender == "mf" or gender == "\\N" or gender == "?":
							#pos_basic = "Egb"
							pos_enriched[0] = "Egb"
						if number == "sg":
							pos_enriched[0] = pos_enriched[0] + "u"
						if number == "pl":
							pos_enriched[0] = pos_enriched[0] + "ll"
					if pos_eurfa == "name":
						pos_basic[0] = "E"					# proper noun
						pos_enriched[0] = "Ep"					# proper noun
						if gender == "m":
							pos_enriched[0] = "Epg"
						if gender == "f":
							pos_enriched[0] = "Epb"
					if pos_eurfa == "det.def":
						pos_basic[0] = "YFB"					# definite article
						pos_enriched[0] = "YFB"				# definite article
					if pos_eurfa == "e" or pos_eurfa == "im":
						pos_basic[0] = "Ebych"					# interjection
						pos_enriched[0] = "Ebych"				# interjection
					if pos_eurfa == "num":
						pos_basic[0] = "Rhi"
						#pos_enriched = "Rhi"
						if extended in ["(0)", "(1)", "(2)", "(3)", "(4)", "(5)", "(6)", "(7)", "(8)", "(9)", "(10)"] or extended in ["one (0)", "one (1)", "two (2)", "three (3)", "four (4)", "five (5)", "six (6)", "seven (7)", "eight (8)", "nine (9)", "ten (10)"]:					# numeral
							pos_enriched[0] = "Rhifol"				# numeral
						else:
							pos_enriched[0] = "Rhifold"
					if pos_eurfa == "ord":
						pos_basic[0] = "Rhi"
						#pos_enriched = "Rhi"
						if extended in ["(1st)", "(2nd)", "(3rd)", "(4th)", "(5th)", "(6th)", "(7th)", "(8th)", "(9th)", "(10th)"]:
							pos_enriched[0] = "Rhitref"					# ordinal
						else:
							pos_enriched[0] = "Rhitrefd"				# ordinal
					if pos_eurfa == "numt":
						pos_basic[0] = "Rhi"
						pos_enriched[0] = "Rhifold"
					if pos_eurfa == "ordt":
						pos_basic[0] = "Rhi"
						pos_enriched[0] = "Rhitrefd"
					if "prt" in pos_eurfa:
						pos_basic[0] = "U"						# unique / unspecified
						if entry[2] == "yn":
							pos_enriched = ["Utra", "Uberf"]
						else:
							pos_enriched[0] = "Utra"					# particle / negative
						if ".neg" in pos_eurfa:
							pos_enriched[0] = "Uneg"
						if ".int" in pos_eurfa:
							pos_enriched[0] = "Ugof"
						if ".aff" in pos_eurfa:
							pos_enriched[0] = "Ucad"
					if pos_eurfa in ["abbrev", "acron", "curr", "percent", "acronym", "letter", "meas"]:
						pos_basic[0] = "Gw"
						if "acron" in pos_eurfa or "acronym" in pos_eurfa:
							pos_enriched[0] = "Gwacr"
						if "abbrev" in pos_eurfa or "meas" in pos_eurfa:
							pos_enriched[0] = "Gwtalf"
						if "curr" in pos_eurfa or "percent" in pos_eurfa:
							pos_enriched[0] = "Gwsym"
						if "letter" in pos_eurfa:
							pos_enriched[0] = "Gwllyth"
					if pos_eurfa == "punc" and corcencc_tag != "" and corcencc_tag != "\\N":
						pos_basic[0] = corcencc_tag.split(" ")[0]
						pos_enriched[0] = corcencc_tag.replace(" ", "")
					if pos_eurfa == "qual" and corcencc_tag != "" and corcencc_tag != "\\N":
						if corcencc_tag == "Adf":
							pos_basic[0] = "Adf"
							pos_enriched[0] = "Adf"
					if pos_eurfa == "preq" and corcencc_tag != "" and corcencc_tag != "\\N":
						if entry[1] in ["unig", "prif", "ambell", "amrwy", "holl"]:
							pos_basic[0] = "Ans"
							pos_enriched = "Ans"
						if entry[1] in ["rhai"]:
							pos_basic[0] = "Rha"
							pos_enriched[0] = "Rha"
						if entry[1] in ["rhyw"]:
							pos_basic[0] = "E"
							pos_enriched[0] = "E"
					if pos_eurfa == "quan" and corcencc_tag != "" and corcencc_tag != "\\N":
						if entry[1] in ["ychydig", "digon", "gormod"]:
							pos_basic[0] = "E"
							pos_enriched[0] = "E"
					#eurfa_tags.append(pos_eurfa)
					if len(pos_basic) == 1 and len(pos_enriched) == 1:
						if pos_basic[0] != "pos_b" and pos_enriched[0] != "pos_e":
							print("{}\t{}\t{}\t{}\t{}".format(entry[1], entry[2], entry[3], pos_basic[0], pos_enriched[0]), file=lexicon)
							extracted_entries.append(entry_id)
					elif len(pos_basic) == 1 and len(pos_enriched) == 2:
						if pos_basic[0] != "pos_b" and pos_enriched[0] != "pos_e" and pos_enriched[1] != "pos_e":
							for rich_pos in pos_enriched:
								print("{}\t{}\t{}\t{}\t{}".format(entry[1], entry[2], entry[3], pos_basic[0], rich_pos), file=lexicon)
							extracted_entries.append(entry_id)
					elif len(pos_basic) == 2 and len(pos_enriched) == 2:
						if pos_basic[0] != "pos_b" and pos_enriched[0] != "pos_e":
							print("{}\t{}\t{}\t{}\t{}".format(entry[1], entry[2], entry[3], pos_basic[0], pos_enriched[0]), file=lexicon)
							extracted_entries.append(entry_id)
						if pos_basic[1] != "pos_b" and pos_enriched[1] != "pos_e":
							print("{}\t{}\t{}\t{}\t{}".format(entry[1], entry[2], entry[3], pos_basic[1], pos_enriched[1]), file=lexicon)
							if entry_id not in extracted_entries:
								extracted_entries.append(entry_id)

	#lexicon = open(lexicon_name, "w")
	##pos_tags_file = open("eurfa_pos_tags", "w")
	#eurfa_tags = []
	#with open(dictionary, newline="") as eurfa_file:
	#	eurfa = csv.reader(eurfa_file, delimiter=",", quotechar="\"")
	#	for entry in eurfa:
	#		#sense = entry[4]
	#		pos_eurfa = entry[4]#[5]
	#		gender = entry[5]#[6]
	#		number = entry[6]#[7]
	#		tense = entry[7]#[8]
	#		extended = entry[12]
	#		pos_basic = "pos_b"
	#		pos_enriched = "pos_e"
	#		if "adj" in pos_eurfa:
	#			pos_basic = "Ans"					#adjective
	#			pos_enriched = "Anscadu"			#adjective
	#			if gender == "f":
	#				pos_enriched = "Anscadbu"
	#			if "pl" in pos_eurfa:
	#				pos_enriched = "Anscadll"
	#			if "eq" in pos_eurfa:
	#				pos_enriched = "Anscyf"
	#			if "comp" in pos_eurfa:
	#				pos_enriched = "Anscym"
	#			if "sup" in pos_eurfa:
	#				pos_enriched = "Anseith"
	#		if pos_eurfa == "adv":
	#			pos_basic = "Adf"					# adverb
	#			pos_enriched = "Adf"				# adverb
	#		if pos_eurfa == "v":
	#			pos_basic = "B"						# verb
	#			#pos_enriched = "B"					# verb
	#			if tense == "infin":
	#				pos_enriched = "Be"
	#			if "pres" in tense:
	#				if number == "1s":
	#					pos_enriched = "Bpres1u"
	#				if number == "2s":
	#					pos_enriched = "Bpres2u"
	#				if number == "3s":
	#					pos_enriched = "Bpres3u"
	#				if number == "1p":
	#					pos_enriched = "Bpres1ll"
	#				if number == "2p":
	#					pos_enriched = "Bpres2ll"
	#				if number == "3p":
	#					pos_enriched = "Bpres3ll"
	#				if number == "0":
	#					pos_enriched = "Bpresamhers"
	#			if tense == "pres.rel":
	#				pos_enriched = "Bpres3perth"
	#			if "fut" in tense:
	#				if number == "1s":
	#					pos_enriched = "Bdyf1u"
	#				if number == "2s":
	#					pos_enriched = "Bdyf2u"
	#				if number == "3s":
	#					pos_enriched = "Bdyf3u"
	#				if number == "1p":
	#					pos_enriched = "Bdyf1ll"
	#				if number == "2p":
	#					pos_enriched = "Bdyf2ll"
	#				if number == "3p":
	#					pos_enriched = "Bdyf3ll"
	#				if number == "0":
	#					pos_enriched = "Bdyfamhers"
	#			if tense == "pluperf":
	#				if number == "1s":
	#					pos_enriched = "Bgorb1u"
	#				if number == "2s":
	#					pos_enriched = "Bgorb2u"
	#				if number == "3s":
	#					pos_enriched = "Bgorb3u"
	#				if number == "1p":
	#					pos_enriched = "Bgorb1ll"
	#				if number == "2p":
	#					pos_enriched = "Bgorb2ll"
	#				if number == "3p":
	#					pos_enriched = "Bgorb3ll"
	#				if number == "0":
	#					pos_enriched = "Bgorbamhers"
	#			if tense == "imperf":
	#				if number == "1s":
	#					pos_enriched = "Bamherff1u"
	#				if number == "2s":
	#					pos_enriched = "Bamherff2u"
	#				if number == "3s":
	#					pos_enriched = "Bamherff3u"
	#				if number == "1p":
	#					pos_enriched = "Bamherff1ll"
	#				if number == "2p":
	#					pos_enriched = "Bamherff2ll"
	#				if number == "3p":
	#					pos_enriched = "Bamherff3ll"
	#				if number == "0":
	#					pos_enriched = "Bamherffamhers"
	#			if tense == "past":
	#				if number == "1s":
	#					pos_enriched = "Bgorff1u"
	#				if number == "2s":
	#					pos_enriched = "Bgorff2u"
	#				if number == "3s":
	#					pos_enriched = "Bgorff3u"
	#				if number == "1p":
	#					pos_enriched = "Bgorff1ll"
	#				if number == "2p":
	#					pos_enriched = "Bgorff2ll"
	#				if number == "3p":
	#					pos_enriched = "Bgorff3ll"
	#				if number == "0":
	#					pos_enriched = "Bgorffamhers"
	#				if number == "123sp":
	#					pos_enriched = "Bgorffsef"
	#			if tense == "imper":
	#				if number == "1s":
	#					pos_enriched = "Bgorch1u"
	#				if number == "2s":
	#					pos_enriched = "Bgorch2u"
	#				if number == "3s":
	#					pos_enriched = "Bgorch3u"
	#				if number == "1p":
	#					pos_enriched = "Bgorch1ll"
	#				if number == "2p":
	#					pos_enriched = "Bgorch2ll"
	#				if number == "3p":
	#					pos_enriched = "Bgorch3ll"
	#				if number == "0":
	#					pos_enriched = "Bgorchamhers"
	#			if tense == "subj":
	#				if number == "1s":
	#					pos_enriched = "Bdibdyf1u"
	#				if number == "2s":
	#					pos_enriched = "Bdibdyf2u"
	#				if number == "3s":
	#					pos_enriched = "Bdibdyf3u"
	#				if number == "1p":
	#					pos_enriched = "Bdibdyf1ll"
	#				if number == "2p":
	#					pos_enriched = "Bdibdyf2ll"
	#				if number == "3p":
	#					pos_enriched = "Bdibdyf3ll"
	#				if number == "0":
	#					pos_enriched = "Bdibdyfamhers"
	#			if tense == "cond":
	#				if number == "1s":
	#					pos_enriched = "Bamod1u"
	#				if number == "2s":
	#					pos_enriched = "Bamod2u"
	#				if number == "3s":
	#					pos_enriched = "Bamod3u"
	#				if number == "1p":
	#					pos_enriched = "Bamod1ll"
	#				if number == "2p":
	#					pos_enriched = "Bamod2ll"
	#				if number == "3p":
	#					pos_enriched = "Bamod3ll"
	#				if number == "0":
	#					pos_enriched = "Bamodamhers"
	#		if "pron" in pos_eurfa:
	#			pos_basic = "Rha"					# pronoun / determiners
	#			#pos_enriched = "Rha"				# pronoun / determiners
	#			if "rel" in pos_eurfa:
	#				pos_enriched = "Rhaperth"
	#			#if number != "":
	#				#pos_enriched = "Rhacyff"
	#			#else:
	#			if number == "1s":
	#				pos_enriched = "Rhapers1u" 
	#			if number == "2s":
	#				pos_enriched = "Rhapers2u" 
	#			if number == "3s":
	#				if gender == "m":
	#					pos_enriched = "Rhapers3gu" 
	#				if gender == "f":
	#					pos_enriched = "Rhapers3bu" 
	#			if number == "1p":
	#				pos_enriched = "Rhapers1ll" 
	#			if number == "2p":
	#				pos_enriched = "Rhapers2ll" 
	#			if number == "3p":
	#				pos_enriched = "Rhapers3ll" 
	#			if number == "sg" or number == "pl":
	#				pos_enriched = "Rhaatb"
	#		if "adj.poss" in pos_eurfa:
	#			pos_basic = "Rha"
	#			pos_enriched = "Rhadib"
	#			if number == "1s":
	#				pos_enriched = "Rhadib1u" 
	#			if number == "2s":
	#				pos_enriched = "Rhadib2u" 
	#			if number == "3s":
	#				if gender == "m":
	#					pos_enriched = "Rhadib3gu" 
	#				if gender == "f":
	#					pos_enriched = "Rhadib3bu" 
	#			if number == "1p":
	#				pos_enriched = "Rhadib1ll" 
	#			if number == "2p":
	#				pos_enriched = "Rhadib2ll" 
	#			if number == "3p":
	#				pos_enriched = "Rhadib3ll"
	#		if "pron.emph" in pos_eurfa:
	#			pos_basic = "Rha"
	#			pos_enriched = "Rhacys"
	#			if number == "1s":
	#				pos_enriched = "Rhacys1u" 
	#			if number == "2s":
	#				pos_enriched = "Rhacys2u" 
	#			if number == "3s":
	#				if gender == "m":
	#					pos_enriched = "Rhacys3gu" 
	#				if gender == "f":
	#					pos_enriched = "Rhacys3bu" 
	#			if number == "1p":
	#				pos_enriched = "Rhacys1ll" 
	#			if number == "2p":
	#				pos_enriched = "Rhacys2ll" 
	#			if number == "3p":
	#				pos_enriched = "Rhacys3ll"
	#		if "adj.dem" in pos_eurfa:
	#			pos_basic = "Rha"					# demonstrative
	#			#pos_enriched = "Rhadang"
	#			if gender == "" or gender == "\n":
	#				pos_enriched = "Rhadangd"
	#			else:
	#				if gender == "m":
	#					pos_enriched = "Rhadangg"
	#				if gender == "f":
	#					pos_enriched = "Rhadangb"
	#			#pos_enriched = "Rhadang"			# demonstrative
	#		if pos_eurfa == "int":
	#			pos_basic = "Rha"					# interrogative
	#			pos_enriched = "Rhagof"				# interrogative
	#		#if pos_eurfa == "quan" or pos_eurfa == "quant":
	#		#	pos_basic = "Rha"					# quantifiers
	#		#	pos_enriched = "Rhames"				# quantifiers
	#		if pos_eurfa == "conj":
	#			pos_basic = "Cys"					# conjunction
	#			pos_enriched = "Cys"				# conjunction
	#		if pos_eurfa == "n":
	#			pos_basic = "E"
	#			#pos_enriched = "E"
	#			if gender == "m":					# noun
	#				#pos_basic = "Eg"
	#				pos_enriched = "Eg"
	#			if gender == "f":
	#				#pos_basic = "Eb"
	#				pos_enriched = "Eb"
	#			if gender == "mf":
	#				#pos_basic = "Egb"
	#				pos_enriched = "Egb"
	#			if number == "sg":
	#				pos_enriched = pos_enriched + "u"
	#			if number == "pl":
	#				pos_enriched = pos_enriched + "ll"
	#		if pos_eurfa == "name":
	#			pos_basic = "E"					# proper noun
	#			pos_enriched = "Ep"					# proper noun
	#			if gender == "m":
	#				pos_enriched = "Epg"
	#			if gender == "f":
	#				pos_enriched = "Epb"
	#		if pos_eurfa == "det.def":
	#			pos_basic = "YFB"					# definite article
	#			pos_enriched = "YFB"				# definite article
	#		if pos_eurfa == "e" or pos_eurfa == "im":
	#			pos_basic = "Ebych"					# interjection
	#			pos_enriched = "Ebych"				# interjection
	#		if pos_eurfa == "num":
	#			pos_basic = "Rhi"
	#			#pos_enriched = "Rhi"
	#			if extended in ["(0)", "(1)", "(2)", "(3)", "(4)", "(5)", "(6)", "(7)", "(8)", "(9)", "(10)"]:					# numeral
	#				pos_enriched = "Rhifol"				# numeral
	#			else:
	#				pos_enriched = "Rhifold"
	#		if pos_eurfa == "ord":
	#			pos_basic = "Rhi"
	#			#pos_enriched = "Rhi"
	#			if extended in ["(1st)", "(2nd)", "(3rd)", "(4th)", "(5th)", "(6th)", "(7th)", "(8th)", "(9th)", "(10th)"]:
	#				pos_enriched = "Rhitref"					# ordinal
	#			else:
	#				pos_enriched = "Rhitrefd"				# ordinal
	#		if "prep" in pos_eurfa:
	#			pos_basic = "Ar"					# preposition
	#			pos_enriched = "Arsym"					# preposition
	#			if pos_eurfa == "prep+pron":
	#				if number == "1s":
	#					pos_enriched == "Ar1u"
	#				if number == "2s":
	#					pos_enriched == "Ar2u"
	#				if number == "3s":
	#					if gender == "f":
	#						pos_enriched = "Ar3bu"
	#					if gender == "m":
	#						pos_enriched = "Ar3gu"
	#					pos_enriched == "Ar3u"
	#				if number == "1p":
	#					pos_enriched == "Ar1ll"
	#				if number == "2p":
	#					pos_enriched == "Ar2ll"
	#				if number == "3p":
	#					pos_enriched == "Ar3ll"
	#		if "prt" in pos_eurfa:
	#			pos_basic = "U"						# unique / unspecified
	#			pos_enriched = "Utra"					# particle / negative
	#			if ".neg" in pos_eurfa:
	#				pos_enriched = "Uneg"
	#			if ".int" in pos_eurfa:
	#				pos_enriched = "Ugof"
	#			if ".aff" in pos_eurfa:
	#				pos_enriched = "Ucad"
	#		if pos_eurfa in ["abbrev", "acron", "curr", "percent", "acronym", "letter"]:
	#			pos_basic = "Gw"
	#			if "acron" in pos_eurfa or "acronym" in pos_eurfa:
	#				pos_enriched = "Gwacr"
	#			if "abbrev" in pos_eurfa:
	#				pos_enriched = "Gwtalf"
	#			if "curr" in pos_eurfa or "percent" in pos_eurfa:
	#				pos_enriched = "Gwsym"
	#			if "letter" in pos_eurfa:
	#				pos_enriched = "Gwllyth"
	#		#eurfa_tags.append(pos_eurfa)
	#		if pos_basic != "pos_b" and pos_enriched != "pos_e":
	#			print("{}\t{}\t{}\t{}\t{}".format(entry[1], entry[2], entry[3], pos_basic, pos_enriched), file=lexicon)
	##eurfa_tags = sorted(set(eurfa_tags))
	##print(eurfa_tags, file=pos_tags_file)

if __name__ == "__main__":
	dictionaries = sys.argv[1:-1]
	lexicon_name = sys.argv[-1]
	if len(dictionaries) == 0:
		print("ERROR: You must include some source dictionaries")
	eurfa_extractor(dictionaries, lexicon_name)