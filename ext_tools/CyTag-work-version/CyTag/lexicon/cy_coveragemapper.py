#!usr/bin/env python3 -tt
#-*- coding: utf-8 -*-
"""
'cy_coveragemapper.py'

Map the frequency of POS tags assigned to tokens in a CyTag-formatted (.xml) output file.

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

cy_coverage = {}

def map_coverage(cytag_output):
	coverage_output = open("CyTag_tag-token_coverage", "w")
	parser = etree.XMLParser(remove_blank_text=True)
	cytag_tree = etree.parse(cytag_output, parser)
	meta_tokens = cytag_tree.xpath("file/paragraph/sentence/token[@id]")
	tokens = list(set([(token.text, token.attrib["basic_pos"], token.attrib["rich_pos"]) for token in meta_tokens if "rich_pos" in token.attrib]))
	tag_pairs = ["E:E", "E:Egu", "E:Ebu", "E:Egll", "E:Ebll", "E:Egbu", "E:Egbll", "E:Ep", "E:Epg", "E:Epb",
			"Ar:Ar", "Ar:Arsym", "Ar:Ar1u", "Ar:Ar2u", "Ar:Ar3gu", "Ar:Ar3bu", "Ar:Ar1ll", "Ar:Ar2ll", "Ar:Ar3ll",
			"Cys:Cys", "Cys:Cyscid", "Cys:Cysis",
			"Rhi:Rhi", "Rhi:Rhifol", "Rhi:Rhifold", "Rhi:Rhifolt", "Rhi:Rhitref", "Rhi:Rhitrefd", "Rhi:Rhitreft",
			"Ans:Ans", "Ans:Anscadu", "Ans:Anscadbu", "Ans:Anscadll", "Ans:Anscyf", "Ans:Anscym", "Ans:Anseith",
			"B:B",	"B:Be", "B:Bpres1u", "B:Bpres2u", "B:Bpres3u", "B:Bpres1ll", "B:Bpres2ll", "B:Bpres3ll", "B:Bpresamhers", "B:Bpres3perth", "B:Bpres3amhen",
					"B:Bdyf1u", "B:Bdyf2u", "B:Bdyf3u", "B:Bdyf1ll", "B:Bdyf2ll", "B:Bdyf3ll", "B:Bdyfamhers",
					"B:Bgorb1u", "B:Bgorb2u", "B:Bgorb3u", "B:Bgorb1ll", "B:Bgorb2ll", "B:Bgorb3ll", "B:Bgorbamhers",
					"B:Bamherff1u", "B:Bamherff2u", "B:Bamherff3u", "B:Bamherff1ll", "B:Bamherff2ll", "B:Bamherff3ll", "B:Bamherffamhers",
					"B:Bgorff1u", "B:Bgorff2u", "B:Bgorff3u", "B:Bgorff1ll", "B:Bgorff2ll", "B:Bgorff3ll", "B:Bgorffamhers", "B:Bgorffsef",
					"B:Bgorch2u", "B:Bgorch3u", "B:Bgorch1ll", "B:Bgorch2ll", "B:Bgorch3ll", "B:Bgorchamhers",
					"B:Bdibdyf1u", "B:Bdibdyf2u", "B:Bdibdyf3u", "B:Bdibdyf1ll", "B:Bdibdyf2ll", "B:Bdibdyf3ll", "B:Bdibdyfamhers",
					"B:Bamod1u", "B:Bamod2u", "B:Bamod3u", "B:Bamod1ll", "B:Bamod2ll", "B:Bamod3ll", "B:Bamodamhers",
			"Rha:Rha", 	"Rha:Rhapers1u", "Rha:Rhapers2u", "Rha:Rhapers3gu", "Rha:Rhapers3bu", "Rha:Rhapers1ll", "Rha:Rhapers2ll", "Rha:Rhapers3ll",
				 	"Rha:Rhadib1u", "Rha:Rhadib2u", "Rha:Rhadib3gu", "Rha:Rhadib3bu", "Rha:Rhadib1ll", "Rha:Rhadib2ll", "Rha:Rhadib3ll",
					"Rha:Rhamedd1u", "Rha:Rhamedd2u", "Rha:Rhamedd3gu", "Rha:Rhamedd3bu", "Rha:Rhamedd1ll", "Rha:Rhamedd2ll", "Rha:Rhamedd3ll",
					"Rha:Rhacys1u", "Rha:Rhacys2u", "Rha:Rhacys3gu", "Rha:Rhacys3bu", "Rha:Rhacys1ll", "Rha:Rhacys2ll", "Rha:Rhacys3ll",
					"Rha:Rhagof", "Rha:Rhadangg", "Rha:Rhadangb", "Rha:Rhadangd", "Rha:Rhaperth", "Rha:Rhaatb", "Rha:Rhacil",
			"U:U", "U:Uneg", "U:Ucad", "U:Ugof", "U:Utra", "U:Uberf",
			"Gw:Gw", "Gw:Gwest", "Gw:Gwfform", "Gw:Gwsym", "Gw:Gwacr", "Gw:Gwtalf", "Gw:Gwdig", "Gw:Gwllyth", "Gw:Gwann",
			"Atd:Atd", "Atd:Atdt", "Atd:Atdcan", "Atd:Atdchw", "Atd:Atdde", "Atd:Atdcys", "Atd:Atddyf",
			"YFB:YFB",
			"Adf:Adf",
			"Ebych:Ebych"]
	matrix = []
	for token in tokens:
		tags = []
		for pair in tag_pairs:
			tags.append(0)
		matrix.append(tags)
	for token in meta_tokens:
		if "basic_pos" in token.attrib and token.attrib["basic_pos"] != "unk" and "rich_pos" in token.attrib and token.attrib["rich_pos"] != "unk" and "{}:{}".format(token.attrib["basic_pos"], token.attrib["rich_pos"]) in tag_pairs:
			token_index = tokens.index((token.text, token.attrib["basic_pos"], token.attrib["rich_pos"]))
			if "{}:{}".format(token.attrib["basic_pos"], token.attrib["rich_pos"]) in tag_pairs:
				pair_index = tag_pairs.index("{}:{}".format(token.attrib["basic_pos"], token.attrib["rich_pos"]))
				if token.text == "goroesi":
					print(pair_index)
				matrix[token_index][pair_index] += 1
	coverage = np.array(matrix)
	for token in tokens:
		if token[2] != "unk" and "{}:{}".format(token[1], token[2]) in tag_pairs:
			pos_index = coverage[tokens.index(token)].argsort()[-1:][::-1]
			cy_coverage[token[0]] = tag_pairs[pos_index[0]]
	json.dump(cy_coverage, coverage_output)


if __name__ == "__main__":
	cytag_output = sys.argv[1]
	map_coverage(cytag_output)