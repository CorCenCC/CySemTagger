#!usr/bin/env python3
#-*- coding: utf-8 -*-
"""
'cy_gazetteer.py'

Extract Welsh gazetteers from DBpedia (Wikipedia).

Accepts as arguments:
	--- REQUIRED:
	--- OPTIONAL:

Developed at Cardiff University as part of the CorCenCC project (www.corcencc.org).

2017 Steve Neale <steveneale3000@gmail.com, NealeS2@cardiff.ac.uk>
"""

import sys
import os
import re

import urllib
from bs4 import BeautifulSoup
import wikipedia

from SPARQLWrapper import SPARQLWrapper, JSON

def extract_gazetteers():
	# PLACES
#	places = []
#	welsh_places = []
#	places_output = open("corcencc.places", "w")
#	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
#	sparql.setReturnFormat(JSON)
#	# Countries
#	sparql.setQuery("select distinct ?label where { ?country rdf:type dbo:Country . ?country rdfs:label ?label . FILTER ( lang(?label) = \"en\") } ")
#	results = sparql.query().convert()["results"]["bindings"]
#	for result in results:
#		places.append(result["label"]["value"].replace(" ", "_"))
#	# City
#	sparql.setQuery("select distinct ?label where { ?country rdf:type dbo:City . ?country rdfs:label ?label . FILTER ( lang(?label) = \"en\") } ")
#	results = sparql.query().convert()["results"]["bindings"]
#	for result in results:
#		places.append(result["label"]["value"].replace(" ", "_"))
#	# PopulatedPlace
#	sparql.setQuery("select distinct ?label where { ?country rdf:type dbo:PopulatedPlace . ?country rdfs:label ?label . FILTER ( lang(?label) = \"en\") } ")
#	results = sparql.query().convert()["results"]["bindings"]
#	for result in results:
#		places.append(result["label"]["value"].replace(" ", "_"))
#	for _i, place in enumerate(places):
#		print("Converting place name {} of {} to Welsh".format(_i+1, len(places)))
#		try:
#			page = BeautifulSoup(urllib.request.urlopen("http://en.wikipedia.org/wiki/{}".format(urllib.parse.quote_plus(place))))
#			if page != None:
#				links = [(el.get('lang'), el.get('title')) for el in page.select("li.interlanguage-link > a")]
#				for language, page_title in links:
#					if language == "cy":
#						title = page_title.split(" – ")[0]
#						print(title, file=places_output)
#		except:
#			pass

	# NAMES
	names = {"given_m": [], "given_f": [], "surnames": []}
	givennames_m_output = open("corcencc.givennames_m", "w")
	givennames_f_output = open("corcencc.givennames_f", "w")
	surnames_output = open("corcencc.surnames", "w")
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setReturnFormat(JSON)
	# Given Names (M)
	sparql.setQuery("select distinct ?label where { ?name rdf:type dbo:GivenName . ?name dbp:gender dbr:Male . ?name rdfs:label ?label . FILTER( lang(?label) = \"en\") }")
	results = sparql.query().convert()["results"]["bindings"]
	for _i, result in enumerate(results):
		print("Recording given name (m) {} of {} to the names dictionary".format(_i+1, len(results)))
		name = result["label"]["value"]
		if " " in name:
			name = name.split(" ")[0]
		names["given_m"].append(name)
		#print(name, file=givennames_m_output)
		sparql.setQuery("select distinct ?label where { ?page rdfs:label \"" + result["label"]["value"] + "\"@en . ?redirect dbo:wikiPageRedirects ?page . ?redirect rdfs:label ?label . FILTER ( lang(?label) = \"en\" ) }")
		redirect_results = sparql.query().convert()["results"]["bindings"]
		for _j, rd_result in enumerate(redirect_results):
			name = rd_result["label"]["value"]
			if " " in name:
				name = name.split(" ")[0]
			names["given_m"].append(name)
			#print(name, file=givennames_m_output)
	sparql.setQuery("select distinct ?label where { ?name rdf:type dbo:GivenName . ?name dct:subject dbc:Masculine_given_names . ?name rdfs:label ?label . FILTER( lang(?label) = \"en\") }")
	results = sparql.query().convert()["results"]["bindings"]
	for _i, result in enumerate(results):
		print("Recording given name (m) {} of {} to the names dictionary".format(_i+1, len(results)))
		name = result["label"]["value"]
		if " " in name:
			name = name.split(" ")[0]
		names["given_m"].append(name)
		#print(name, file=givennames_m_output)
		sparql.setQuery("select distinct ?label where { ?page rdfs:label \"" + result["label"]["value"] + "\"@en . ?redirect dbo:wikiPageRedirects ?page . ?redirect rdfs:label ?label . FILTER ( lang(?label) = \"en\" ) }")
		redirect_results = sparql.query().convert()["results"]["bindings"]
		for _j, rd_result in enumerate(redirect_results):
			name = rd_result["label"]["value"]
			if " " in name:
				name = name.split(" ")[0]
			names["given_m"].append(name)
			#print(name, file=givennames_m_output)
	sparql.setQuery("select distinct ?label where { ?region_name skos:broader dbc:Masculine_given_names . ?country_name skos:broader ?region_name . ?name rdf:type dbo:GivenName . ?name dct:subject ?country_name . ?name rdfs:label ?label . FILTER( lang(?label) = \"en\") }")
	results = sparql.query().convert()["results"]["bindings"]
	for _i, result in enumerate(results):
		print("Recording given name (m) {} of {} to the names dictionary".format(_i+1, len(results)))
		name = result["label"]["value"]
		if " " in name:
			name = name.split(" ")[0]
		names["given_m"].append(name)
		#print(name, file=givennames_m_output)
		sparql.setQuery("select distinct ?label where { ?page rdfs:label \"" + result["label"]["value"] + "\"@en . ?redirect dbo:wikiPageRedirects ?page . ?redirect rdfs:label ?label . FILTER ( lang(?label) = \"en\" ) }")
		redirect_results = sparql.query().convert()["results"]["bindings"]
		for _j, rd_result in enumerate(redirect_results):
			name = rd_result["label"]["value"]
			if " " in name:
				name = name.split(" ")[0]
			names["given_m"].append(name)
			#print(name, file=givennames_m_output)
	# Given Names (F)
	sparql.setQuery("select distinct ?label where { ?name rdf:type dbo:GivenName . ?name dbp:gender dbr:Female . ?name rdfs:label ?label . FILTER( lang(?label) = \"en\") }")
	results = sparql.query().convert()["results"]["bindings"]
	for _i, result in enumerate(results):
		print("Recording given name (f) {} of {} to the names dictionary".format(_i+1, len(results)))
		name = result["label"]["value"]
		if " " in name:
			name = name.split(" ")[0]
		names["given_f"].append(name)
		#print(name, file=givennames_f_output)
		sparql.setQuery("select distinct ?label where { ?page rdfs:label \"" + result["label"]["value"] + "\"@en . ?redirect dbo:wikiPageRedirects ?page . ?redirect rdfs:label ?label . FILTER ( lang(?label) = \"en\" ) }")
		redirect_results = sparql.query().convert()["results"]["bindings"]
		for _j, rd_result in enumerate(redirect_results):
			name = rd_result["label"]["value"]
			if " " in name:
				name = name.split(" ")[0]
			names["given_f"].append(name)
			#print(name, file=givennames_f_output)
	sparql.setQuery("select distinct ?label where { ?name rdf:type dbo:GivenName . ?name dct:subject dbc:Feminine_given_names . ?name rdfs:label ?label . FILTER( lang(?label) = \"en\") }")
	results = sparql.query().convert()["results"]["bindings"]
	for _i, result in enumerate(results):
		print("Recording given name (f) {} of {} to the names dictionary".format(_i+1, len(results)))
		name = result["label"]["value"]
		if " " in name:
			name = name.split(" ")[0]
		names["given_f"].append(name)
		#print(name, file=givennames_f_output)
		sparql.setQuery("select distinct ?label where { ?page rdfs:label \"" + result["label"]["value"] + "\"@en . ?redirect dbo:wikiPageRedirects ?page . ?redirect rdfs:label ?label . FILTER ( lang(?label) = \"en\" ) }")
		redirect_results = sparql.query().convert()["results"]["bindings"]
		for _j, rd_result in enumerate(redirect_results):
			name = rd_result["label"]["value"]
			if " " in name:
				name = name.split(" ")[0]
			names["given_f"].append(name)
			#print(name, file=givennames_f_output)
	sparql.setQuery("select distinct ?label where { ?region_name skos:broader dbc:Feminine_given_names . ?country_name skos:broader ?region_name . ?name rdf:type dbo:GivenName . ?name dct:subject ?country_name . ?name rdfs:label ?label . FILTER( lang(?label) = \"en\") }")
	results = sparql.query().convert()["results"]["bindings"]
	for _i, result in enumerate(results):
		print("Recording given name (f) {} of {} to the names dictionary".format(_i+1, len(results)))
		name = result["label"]["value"]
		if " " in name:
			name = name.split(" ")[0]
		names["given_f"].append(name)
		#print(name, file=givennames_f_output)
		sparql.setQuery("select distinct ?label where { ?page rdfs:label \"" + result["label"]["value"] + "\"@en . ?redirect dbo:wikiPageRedirects ?page . ?redirect rdfs:label ?label . FILTER ( lang(?label) = \"en\" ) }")
		redirect_results = sparql.query().convert()["results"]["bindings"]
		for _j, rd_result in enumerate(redirect_results):
			name = rd_result["label"]["value"]
			if " " in name:
				name = name.split(" ")[0]
			names["given_f"].append(name)
			#print(name, file=givennames_f_output)
	# Surnames
	sparql.setQuery("select distinct ?label where { ?lang_surname skos:broader dbc:Surnames_by_language . ?surname dct:subject ?lang_surname . ?surname rdfs:label ?label . FILTER( lang(?label) = \"en\") }")
	results = sparql.query().convert()["results"]["bindings"]
	for _i, result in enumerate(results):
		print("Recording surname {} of {} to the names dictionary".format(_i+1, len(results)))
		name = result["label"]["value"]
		if " " in name:
			name = name.split(" ")[0]
		names["surnames"].append(name)
		#print(name, file=surnames_output)
	sparql.setQuery("select distinct ?s ?label where { ?s rdfs:label ?label . FILTER( lang(?label) = \"en\" ) . ?label bif:contains \"(surname)\"  }")
	results = sparql.query().convert()["results"]["bindings"]
	for _i, result in enumerate(results):
		print("Recording surname {} of {} to the names dictionary".format(_i+1, len(results)))
		name = result["label"]["value"]
		if " " in name:
			name = name.split(" ")[0]
		names["surnames"].append(name)
		#print(name, file=surnames_output)
	for gaz in names.keys():
		names[gaz] = set(names[gaz])
	for _i, entry in enumerate(names["given_m"]):
		print("Writing masculine name {} of {} to the output gazetteer file".format(_i+1, len(names["given_m"])))
		print(entry, file=givennames_m_output)
	for _i, entry in enumerate(names["given_f"]):
		print("Writing feminine name {} of {} to the output gazetteer file".format(_i+1, len(names["given_f"])))
		print(entry, file=givennames_f_output)
	for _i, entry in enumerate(names["surnames"]):
		print("Writing surname name {} of {} to the output gazetteer file".format(_i+1, len(names["surnames"])))
		print(entry, file=surnames_output)


if __name__ == "__main__":
	extract_gazetteers()