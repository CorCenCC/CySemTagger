import sys
import os

from urllib import parse

def get_lines(input_data):
	# Create an empty list to hold the line data
	line_data = []
	if isinstance(input_data, list):
		# If the input is a list of files...
		for file_id, file in enumerate(input_data):
			# Split each opened file into lines and append them to the line data
			with open(file) as file_text:
				line_data.append([file, file_text.read().splitlines()])
	elif isinstance(input_data, str):
		input_text = parse.unquote(input_data)
		# If the input is a string, split the input string into lines and use them as the line data
		line_data = [["N/A", input_text.replace("\\n", "\n").splitlines()]]
	# Return the line data
	return(line_data)