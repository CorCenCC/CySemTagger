#!usr/bin/env python3 -tt
#-*- coding: utf-8 -*-
"""
'cy_tagsequence_mapper.py'

Map the frequency of n-gram sequences of POS tags in a CyTag-formatted (.xml) output file.

Accepts as arguments:
	--- REQUIRED: A CyTag-formatted (.xml) output file
	--- OPTIONAL:

Developed at Cardiff University as part of the CorCenCC project (www.corcencc.org).

2016-2017 Steve Neale <steveneale3000@gmail.com, NealeS2@cardiff.ac.uk>
"""

import sys
import os

from lxml import etree
import numpy as np

import json

n_grams = {}

def map_tagsequences(cytag_output):
	tagsequence_output = open("CyTag_tag-sequences", "w")
	parser = etree.XMLParser(remove_blank_text=True)
	cytag_tree = etree.parse(cytag_output, parser)
	sentences = cytag_tree.xpath("file/paragraph/sentence[@id]")
	print(len(sentences))
	for i, sentence in enumerate(sentences):
		tokens = sentence.xpath("token[@id]")
		if len(tokens) > 2:	
			for j, token in enumerate(tokens):
				if j == 0: 
					if "rich_pos" in token.attrib and "rich_pos" in tokens[j+1].attrib and "rich_pos" in tokens[j+2].attrib:
						if str(["find", tokens[j+1].attrib["rich_pos"], tokens[j+2].attrib["rich_pos"]]) not in n_grams.keys() and "unk" not in str(["find", tokens[j+1].attrib["rich_pos"], tokens[j+2].attrib["rich_pos"]]) and token.attrib["rich_pos"] != "unk":
							n_grams[str(["find", tokens[j+1].attrib["rich_pos"], tokens[j+2].attrib["rich_pos"]])] = token.attrib["rich_pos"]
				elif j == len(tokens)-1: 
					if "rich_pos" in token.attrib and "rich_pos" in tokens[j-2].attrib and "rich_pos" in tokens[j-1].attrib:
						if str([tokens[j-2].attrib["rich_pos"], tokens[j-1].attrib["rich_pos"], "find"]) not in n_grams.keys() and "unk" not in str([tokens[j-2].attrib["rich_pos"], tokens[j-1].attrib["rich_pos"], "find"]) and token.attrib["rich_pos"] != "unk":
							n_grams[str([tokens[j-2].attrib["rich_pos"], tokens[j-1].attrib["rich_pos"], "find"])] = token.attrib["rich_pos"]
				else:
					if "rich_pos" in token.attrib and "rich_pos" in tokens[j-1].attrib and "rich_pos" in tokens[j+1].attrib:
						if str([tokens[j-1].attrib["rich_pos"], "find", tokens[j+1].attrib["rich_pos"]]) not in n_grams.keys() and "unk" not in str([tokens[j-1].attrib["rich_pos"], "find", tokens[j+1].attrib["rich_pos"]]) and token.attrib["rich_pos"] != "unk":
							n_grams[str([tokens[j-1].attrib["rich_pos"], "find", tokens[j+1].attrib["rich_pos"]])] = token.attrib["rich_pos"]
	json.dump(n_grams, tagsequence_output)
	#meta_tokens = cytag_tree.xpath("file/paragraph/sentence/token[@id]")
	#tokens = list(set([token.text for token in meta_tokens]))
	#tag_pairs = ["E:E", "E:Egu", "E:Ebu", "E:Egll", "E:Ebll", "E:Egbu", "E:Egbll", "E:Ep", "E:Epg", "E:Epb",
	#		"Ar:Ar", "Ar:Arsym", "Ar:Ar1u", "Ar:Ar2u", "Ar:Ar3gu", "Ar:Ar3bu", "Ar:Ar1ll", "Ar:Ar2ll", "Ar:Ar3ll",
	#		"Cys:Cys", "Cys:Cyscid", "Cys:Cysis",
	#		"Rhi:Rhi", "Rhi:Rhifol", "Rhi:Rhifold", "Rhi:Rhifolt", "Rhi:Rhitref", "Rhi:Rhitrefd", "Rhi:Rhitreft",
	#		"Ans:Ans", "Ans:Anscadu", "Ans:Anscadbu", "Ans:Anscadll", "Ans:Anscyf", "Ans:Anscym", "Ans:Anseith",
	#		"B:B",	"B:Be ", "B:Bpresdyf1u", "B:Bpresdyf2u", "B:Bpresdyf3u", "B:Bpresdyf1ll", "B:Bpresdyf2ll", "B:Bpresdyf3ll", "B:Bpresdyfamhers", "B:Bpresdyf3perth",
	#				"B:Bgorb1u", "B:Bgorb2u", "B:Bgorb3u", "B:Bgorb1ll", "B:Bgorb2ll", "B:Bgorb3ll", "B:Bgorbamhers",
	#				"B:Bamhen1u", "B:Bamhen2u", "B:Bamhen3u", "B:Bamhen1ll", "B:Bamhen2ll", "B:Bamhen3ll", "B:Bamhenamhers",
	#				"B:Bgorff1u", "B:Bgorff2u", "B:Bgorff3u", "B:Bgorff1ll", "B:Bgorff2ll", "B:Bgorff3ll", "B:Bgorffamhers", "B:Bgorffsef",
	#				"B:Bgorch2u", "B:Bgorch3u", "B:Bgorch1ll", "B:Bgorch2ll", "B:Bgorch3ll", "B:Bgorchamhers",
	#				"B:Bdibdyf1u", "B:Bdibdyf2u", "B:Bdibdyf3u", "B:Bdibdyf1ll", "B:Bdibdyf2ll", "B:Bdibdyf3ll", "B:Bdibdyfamhers",
	#				"B:Bamod1u", "B:Bamod2u", "B:Bamod3u", "B:Bamod1ll", "B:Bamod2ll", "B:Bamod3ll", "B:Bamodamhers",
	#		"Rha:Rha", 	"Rha:Rhapers1u", "Rha:Rhapers2u", "Rha:Rhapers3gu", "Rha:Rhapers3bu", "Rha:Rhapers1ll", "Rha:Rhapers2ll", "Rha:Rhapers3ll",
	#			 	"Rha:Rhadib1u", "Rha:Rhadib2u", "Rha:Rhadib3gu", "Rha:Rhadib3bu", "Rha:Rhadib1ll", "Rha:Rhadib2ll", "Rha:Rhadib3ll",
	#				"Rha:Rhamedd1u", "Rha:Rhamedd2u", "Rha:Rhamedd3gu", "Rha:Rhamedd3bu", "Rha:Rhamedd1ll", "Rha:Rhamedd2ll", "Rha:Rhamedd3ll",
	#				"Rha:Rhacys1u", "Rha:Rhacys2u", "Rha:Rhacys3gu", "Rha:Rhacys3bu", "Rha:Rhacys1ll", "Rha:Rhacys2ll", "Rha:Rhacys3ll",
	#				"Rha:Rhagof", "Rha:Rhadangg", "Rha:Rhadangb", "Rha:Rhadangd", "Rha:Rhaperth", "Rha:Rhaatb", "Rha:Rhacil",
	#		"U:U", "U:Uneg", "U:Ucad", "U:Ugof", "U:Utra",
	#		"Gw:Gw", "Gw:Gwest", "Gw:Gwfform", "Gw:Gwsym", "Gw:Gwacr", "Gw:Gwtalf", "Gw:Gwdig", "Gw:Gwllyth", "Gw:Gwann",
	#		"Atd:Atd", "Atd:Atdt", "Atd:Atdcan", "Atd:Atdchw", "Atd:Atdde", "Atd:Atdcys", "Atd:Atddyf",
	#		"YFB:YFB",
	#		"Adf:Adf",
	#		"Ebych:Ebych"]
	#matrix = []
	#for token in tokens:
	#	tags = []
	#	for pair in tag_pairs:
	#		tags.append(0)
	#	matrix.append(tags)
	#for token in meta_tokens:
	#	if "basic_pos" in token.attrib and "rich_pos" in token.attrib:
	#		token_index = tokens.index(token.text)
	#		if "{}:{}".format(token.attrib["basic_pos"], token.attrib["rich_pos"]) in tag_pairs:
	#			pair_index = tag_pairs.index("{}:{}".format(token.attrib["basic_pos"], token.attrib["rich_pos"]))
	#			matrix[token_index][pair_index] += 1
	#coverage = np.array(matrix)
	#for token in tokens:
	#	pos_index = coverage[tokens.index(token)].argsort()[-1:][::-1]
	#	cy_coverage[token] = tag_pairs[pos_index[0]]
	#json.dump(cy_coverage, coverage_output)


if __name__ == "__main__":
	cytag_output = sys.argv[1]
	map_tagsequences(cytag_output)