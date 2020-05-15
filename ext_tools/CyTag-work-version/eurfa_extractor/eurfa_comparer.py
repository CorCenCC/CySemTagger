import sys
import os
import re
import csv

basic_tags = {
		"Egu": "E",
		"YFB": "YFB",
		"Arsym": "Ar",
		"Cyscyd": "Cys",
		"Rhifol": "Rhi",
		"Anscadu": "Ans",
		"Adf": "Adf",
		"Be": "B",
		"Rhapers1u": "Rha",
		"Uneg": "U",
		"Ebych": "Ebych",
		"Gwest": "Gw",
		"Atdt": "Atd",
}

tag_dict = {
		"Egu": "E",
		"Ebu": "E",
		"Egll": "E",
		"Ebll": "E",
		"Egbu": "E",
		"Egbll": "E",
		"Ep": "E",
		"Epg": "E",
		"Epb": "E",
		"YFB": "YFB",
		"Arsym": "Ar",
		"Ar1u": "Ar",
		"Ar2u": "Ar",
		"Ar3gu": "Ar",
		"Ar3bu": "Ar",
		"Ar1ll": "Ar",
		"Ar2ll": "Ar",
		"Ar3ll": "Ar",
		"Cyscyd": "Cys",
		"Cysis": "Cys",
		"Rhifol": "Rhi",
		"Rhifold": "Rhi",
		"Rhifolt": "Rhi",
		"Rhitref": "Rhi",
		"Rhitrefd": "Rhi",
		"Rhitreft": "Rhi",
		"Anscadu": "Ans",
		"Anscadbu": "Ans",
		"Anscadll": "Ans",
		"Anscyf": "Ans",
		"Anscym": "Ans",
		"Anseith": "Ans",
		"Adf": "Adf",
		"Be": "B",
		"Bpres1u": "B",
		"Bpres2u": "B",
		"Bpres3u": "B",
		"Bpres1ll": "B",
		"Bpres2ll": "B",
		"Bpres3ll": "B",
		"Bpresamhers": "B",
		"Bpres3perth": "B",
		"Bpres3amhen": "B",
		"Bdyf1u": "B",
		"Bdyf2u": "B",
		"Bdyf3u": "B",
		"Bdyf1ll": "B",
		"Bdyf2ll": "B",
		"Bdyf3ll": "B",
		"Bdyfamhers": "B",
		"Bgorb1u": "B",
		"Bgorb2u": "B",
		"Bgorb3u": "B",
		"Bgorb1ll": "B",
		"Bgorb2ll": "B",
		"Bgorb3ll": "B",
		"Bgorbamhers": "B",
		"Bamherff1u": "B",
		"Bamherff2u": "B",
		"Bamherff3u": "B",
		"Bamherff1ll": "B",
		"Bamherff2ll": "B",
		"Bamherff3ll": "B",
		"Bamherffamhers": "B",
		"Bgorff1u": "B",
		"Bgorff2u": "B",
		"Bgorff3u": "B",
		"Bgorff1ll": "B",
		"Bgorff2ll": "B",
		"Bgorff3ll": "B",
		"Bgorffamhers": "B",
		"Bgorffsef": "B",
		"Bgorch2u": "B",
		"Bgorch3u": "B",
		"Bgorch1ll": "B",
		"Bgorch2ll": "B",
		"Bgorch3ll": "B",
		"Bgorchamhers": "B",
		"Bdibdyf1u": "B",
		"Bdibdyf2u": "B",
		"Bdibdyf3u": "B",
		"Bdibdyf1ll": "B",
		"Bdibdyf2ll": "B",
		"Bdibdyf3ll": "B",
		"Bdibdyfamhers": "B",
		"Bamod1u": "B",
		"Bamod2u": "B",
		"Bamod3u": "B",
		"Bamod1ll": "B",
		"Bamod2ll": "B",
		"Bamod3ll": "B",
		"Bamodamhers": "B",
		"Rhapers1u": "Rha",
		"Rhapers2u": "Rha",
		"Rhapers3gu": "Rha",
		"Rhapers3bu": "Rha",
		"Rhapers1ll": "Rha",
		"Rhapers2ll": "Rha",
		"Rhapers3ll": "Rha",
		"Rhadib1u": "Rha",
		"Rhadib2u": "Rha",
		"Rhadib3gu": "Rha",
		"Rhadib3bu": "Rha",
		"Rhadib1ll": "Rha",
		"Rhadib2ll": "Rha",
		"Rhadib3ll": "Rha",
		"Rhamedd1u": "Rha",
		"Rhamedd2u": "Rha",
		"Rhamedd3gu": "Rha",
		"Rhamedd3bu": "Rha",
		"Rhamedd1ll": "Rha",
		"Rhamedd2ll": "Rha",
		"Rhamedd3ll": "Rha",
		"Rhacys1u": "Rha",
		"Rhacys2u": "Rha",
		"Rhacys3gu": "Rha",
		"Rhacys3bu": "Rha",
		"Rhacys1ll": "Rha",
		"Rhacys2ll": "Rha",
		"Rhacys3ll": "Rha",
		"Rhagof": "Rha",
		"Rhadangg": "Rha",
		"Rhadangb": "Rha",
		"Rhadangd": "Rha",
		"Rhaperth": "Rha",
		"Rhaatb": "Rha",
		"Rhacil": "Rha",
		"Uneg": "U",
		"Ucad": "U",
		"Ugof": "U",
		"Utra": "U",
		"Uberf": "U",
		"Ebych": "Ebych",
		"Gwest": "Gw",
		"Gwfform": "Gw",
		"Gwsym": "Gw",
		"Gwacr": "Gw",
		"Gwtalf": "Gw",
		"Gwdig": "Gw",
		"Gwllyth": "Gw",
		"Gwrhuf": "Gw",
		"Gwann": "Gw",
		"Atdt": "Atd",
		"Atdcan": "Atd",
		"Atdchw": "Atd",
		"Atdde": "Atd",
		"Atdcys": "Atd",
		"Atddyf": "Atd"
}

def compare_lexicon(dictionaries, lexicon_name):
	missing_entries = open("missing_eurfa_entries", "w")
	missing_types = open("missing_eurfa_types", "w")
	output = open("eurfa_comparer_output", "w")
	with open(lexicon_name) as loaded_lexicon:
		
		lexicon = loaded_lexicon.read().splitlines()
		dict_names = [line[6:] for line in lexicon if line[:5] == "# ---"]
		print(dict_names)
		if dictionaries == dict_names:
			print("True")
		else:
			print("ERROR: The supplied dictionaries do not match the dictionaries used in the supplied lexicon")
			return
		lexicon_dicts = []
		for _i, dictionary in enumerate(dictionaries):
			if _i < len(dictionaries)-1:
				start = lexicon.index("### {} ###".format(dictionaries[_i]))+1
				end = lexicon.index("### {} ###".format(dictionaries[_i+1]))
				lexicon_dicts.append(lexicon[start:end])
			else:
				start = lexicon.index("### {} ###".format(dictionaries[_i]))+1
				lexicon_dicts.append(lexicon[start:])
		lexicon_dicts = list(filter(None, lexicon_dicts))
		for _i, dictionary in enumerate(lexicon_dicts):
			correct_rich = 0
			wrong_rich = 0
			for _j, entry in enumerate(dictionary):
				parts = entry.split("\t")
				if parts[4] not in tag_dict.keys():
					wrong_rich += 1
					print("{}: {}".format(parts[0], parts[4]))
				else:
					correct_rich += 1
			print("From {} entries in {}, {} have a valid enriched tag".format(len(dictionary), dictionaries[_i], correct_rich))
			print(dictionaries[_i], len(dictionary))
		already_extracted = []
		for _i, dictionary in enumerate(dictionaries):
			print("### {} ###".format(dictionary), file=missing_entries)
			print("### {} ###".format(dictionary), file=missing_types)
			already_there = 0
			missing_count = 0
			skipped = 0
			missing_type_list = []
			current_lexicon = lexicon_dicts[_i]
			with open(dictionary) as loaded_dict:
				current_dict = list(csv.reader(loaded_dict, delimiter=",", quotechar="\""))
				print(len(current_lexicon), file=output)
				for _j, entry in enumerate(current_dict[1:]):
					index = _j - skipped
					dict_entryid = entry[0]
					dict_token = entry[1]
					dict_lemmas = [entry[2], entry[3]]
					lexicon_token = current_lexicon[index - (missing_count+already_there)].split("\t")[0] if int(index - (missing_count+already_there)) < len(current_lexicon) else ""
					lexicon_lemmas = [current_lexicon[index - (missing_count+already_there)].split("\t")[1], current_lexicon[index - (missing_count+already_there)].split("\t")[2]] if int(index - (missing_count+already_there)) < len(current_lexicon) else []
					print(index, missing_count)
					print("{} {} {} {}".format(index, missing_count, dict_token, lexicon_token), file=output)
					
					if dict_entryid in already_extracted:
						if dict_token != lexicon_token:
							already_there += 1
							next_comparison = "Next is {} and {}".format(current_dict[1:][index+1][1], current_lexicon[index+1 - (missing_count+already_there)].split("\t")[0]) if int(index+1 - (missing_count+already_there)) < len(current_lexicon) else ""
							print(index, missing_count, "Already there! {}".format(next_comparison), file=output)
						else:
							#already_there += 1
							next_comparison = "Next is {} and {}".format(current_dict[1:][index][1], current_lexicon[index - (missing_count+already_there)].split("\t")[0]) if int(index - (missing_count+already_there)) < len(current_lexicon) else ""
							print(index, missing_count, "Already there! {}".format(next_comparison), file=output)	
							if dict_lemmas != lexicon_lemmas:
							#	already_there += 1
							#else:
								skipped += 1
					else:
						if dict_token != lexicon_token:
							missing_count += 1
							next_comparison = "Next is {} and {}".format(current_dict[1:][index+1][1], current_lexicon[index+1 - (missing_count+already_there)].split("\t")[0]) if int(index+1 - (missing_count+already_there)) < len(current_lexicon) else ""
							print(index, missing_count, "Actually missing. {}".format(next_comparison), file=output)
							print(entry, file=missing_entries)
							if len(entry) == 19:
								if [entry[4], entry[5], entry[6], entry[7], entry[13]] not in missing_type_list:
									missing_type_list.append([entry[4], entry[5], entry[6], entry[7], entry[13]])
							if len(entry) == 11:
								if [entry[5], entry[6], entry[7], entry[8]] not in missing_type_list:
									missing_type_list.append([entry[5], entry[6], entry[7], entry[8]])


					#if dict_token != lexicon_token:
					#	if dict_entryid in already_extracted:
					#		already_there += 1
					#		next_comparison = "Next is {} and {}".format(current_dict[1:][_j+1][1], current_lexicon[_j+1 - (missing_count+already_there)].split("\t")[0]) if int(_j+1 - (missing_count+already_there)) < len(current_lexicon) else ""
					#		print(_j, missing_count, "Already there! {}".format(next_comparison), file=output)
					#	else:
					#		missing_count += 1
					#		next_comparison = "Next is {} and {}".format(current_dict[1:][_j+1][1], current_lexicon[_j+1 - (missing_count+already_there)].split("\t")[0]) if int(_j+1 - (missing_count+already_there)) < len(current_lexicon) else ""
					#		print(_j, missing_count, "Actually missing. {}".format(next_comparison), file=output)
					#		print(entry, file=missing_entries)
					#		if len(entry) == 19:
					#			if [entry[4], entry[5], entry[6], entry[7], entry[13]] not in missing_type_list:
					#				missing_type_list.append([entry[4], entry[5], entry[6], entry[7], entry[13]])
					#		if len(entry) == 11:
					#			if [entry[5], entry[6], entry[7], entry[8]] not in missing_type_list:
					#				missing_type_list.append([entry[5], entry[6], entry[7], entry[8]])
					#else:
					#	if dict_entryid in already_extracted:
					#		#already_there += 1
					#		next_comparison = "Next is {} and {}".format(current_dict[1:][_j+1][1], current_lexicon[_j+1 - (missing_count+already_there)].split("\t")[0]) if int(_j+1 - (missing_count+already_there)) < len(current_lexicon) else ""
					#		print(_j, missing_count, "Already there! {}".format(next_comparison), file=output)
					
					if dict_entryid not in already_extracted:
						already_extracted.append(dict_entryid)
				for missing_type in missing_type_list:
					print(missing_type, file=missing_types)
				print("There are {} entries in '{}' ({}) not present in the extracted lexicon ({})".format(missing_count, dictionary, len(open(dictionary).readlines()), len(current_lexicon)), file=output)
			print("{} entries were already there".format(already_there), file=output)

		#for _i, entry in enumerate(eurfa):
		#		eurfa_token = entry[1]
		#		lexicon_token = lexicon[_i - missing_count].split("\t")[0]
		#		if eurfa_token != lexicon_token:
		#			missing_count += 1
		#			print(entry, file=missing_entries)
		#			if [entry[4], entry[5], entry[6], entry[7], entry[13]] not in missing_type_list:
		#				missing_type_list.append([entry[4], entry[5], entry[6], entry[7], entry[13]])
		#	for missing_type in missing_type_list:
		#		print(missing_type, file=missing_types)
		#	print("There are {} entries in Eurfa ({}) not present in the extracted lexicon ({})".format(missing_count, len(open(eurfa_file).readlines()), len(lexicon)))

def compare(lexicon_name, eurfa_file):
	missing_entries = open("missing_eurfa_entries", "w")
	missing_types = open("missing_eurfa_types", "w")
	with open(eurfa_file) as loaded_eurfa:
		eurfa = csv.reader(loaded_eurfa, delimiter=",", quotechar="\"")
		with open(lexicon_name) as loaded_lexicon:
			lexicon = loaded_lexicon.read().splitlines()
			correct_rich = 0
			wrong_rich = 0
			for _i, entry in enumerate(lexicon):
				if entry[0] != "#":
					parts = entry.split("\t")
					if parts[4] not in tag_dict.keys():
					   wrong_rich += 1
					   print("{}: {}".format(parts[0], parts[4]))
					else:
					   correct_rich += 1
			print("From {} lexicon entries, {} have a valid enriched tag".format(len(lexicon), correct_rich))
			missing_count = 0
			missing_type_list = []
			for _i, entry in enumerate(eurfa):
				eurfa_token = entry[1]
				lexicon_token = lexicon[_i - missing_count].split("\t")[0]
				if eurfa_token != lexicon_token:
					missing_count += 1
					print(entry, file=missing_entries)
					if [entry[4], entry[5], entry[6], entry[7], entry[13]] not in missing_type_list:
						missing_type_list.append([entry[4], entry[5], entry[6], entry[7], entry[13]])
			for missing_type in missing_type_list:
				print(missing_type, file=missing_types)
			print("There are {} entries in Eurfa ({}) not present in the extracted lexicon ({})".format(missing_count, len(open(eurfa_file).readlines()), len(lexicon)))

if __name__ == "__main__":
	dictionaries = sys.argv[1:-1]
	lexicon_name = sys.argv[-1]
	if len(dictionaries) == 0:
		print("ERROR: You must include some source dictionaries")
	compare_lexicon(dictionaries, lexicon_name)

#if __name__ == "__main__":
#	lexicon_name = sys.argv[1]
#	eurfa_file = sys.argv[2]
#	#compare(lexicon_name, eurfa_file)