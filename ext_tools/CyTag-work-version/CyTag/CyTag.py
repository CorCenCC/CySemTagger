#!usr/bin/env python3
#-*- coding: utf-8 -*-
"""
'CyTag.py'

A surface-level natural language processing pipeline for Welsh texts (text segmentation -> sentence splitting -> tokenisation -> part-of-speech (POS) tagging).

CyTag can either process Welsh text via standard input, or accepts the following sequences of arguments:
	--- REQUIRED: A string of Welsh language text.
	or:
	--- REQUIRED: One or more Welsh input text files (raw text).
	--- REQUIRED: A name to describe the corpus and its output files.
	--- OPTIONAL: A directory in which output files will be saved.
	--- OPTIONAL: A specific component to run the pipeline to, should running the entire pipeline not be required ('seg', 'sent', 'tok', 'pos').
	--- REQUIRED: A format to write the pipeline's output ('tsv', 'xml' or 'all')
	or:
	--- REQUIRED: 'evaluate'
	--- OPTIONAL: 'soft' (for a more lenient evaluation of CyTag output).
	--- REQUIRED: A gold standard (CyTag XML-formatted) dataset. 
	--- REQUIRED: XML-formatted CyTag output to be evaluated.

Developed at Cardiff University as part of the CorCenCC project (www.corcencc.org).

2016-2017 Steve Neale <steveneale3000@gmail.com, NealeS2@cardiff.ac.uk>, Kevin Donnelly <kevin@dotmon.com>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses>.
"""

import sys
import os
sys.path.insert(0, "{}/src/".format(os.path.dirname(os.path.abspath(__file__))))

from cy_taggedobject import taggedobject
from cy_textsegmenter import *
from cy_sentencesplitter import *
from cy_tokeniser import *
from cy_postagger import *

from evaluate_cytag import *

def process(arguments):
	# Create an empty output object
	output = taggedobject()
	# If more than one argument was passed...
	if len(arguments) > 1: 
		# If the fourth argument was not empty, return the output of the appropriate pipeline component ('seg', 'sent', 'tok', 'pos')
		if arguments[3] != None:
			if arguments[3] == "seg":
				output = segment_text(arguments[0], output)
			elif arguments[3] == "sent":
				output = sentence_splitter(arguments[0], output)
			elif arguments[3] == "tok":
				output = tokeniser(arguments[0], output)
			elif arguments[3] == "pos":
				output = pos_tagger(arguments[:3], arguments[4], output)
		# Otherwise...
		else:
			# Return the output of the POS tagger
			output = pos_tagger(arguments[:3], arguments[4], output)
		# If the returned output is a 'cy_taggedobject'...
		if isinstance(output, taggedobject):
			# If the fourth argument was not 'None' and was either 'tok' or 'pos'...
			if arguments[3] == None or arguments[3] in ["tok", "pos"]:
				# Pring the output object to the appropriate file format(s)
				output.print_to_file(arguments[1], arguments[2], arguments[4])
	# Otherwise (assuming the passed argument to have been a single string)...
	else:
		# Run the POS tagger, and print the output object to standard output
		output = pos_tagger(arguments, None, output)
		output.print_to_stdout()

if __name__ == "__main__":
	args = sys.argv[1:]
	# If no arguments were passed:
	if len(args) == 0:
		# Alert the user if nothing has been passed to the program via standard input
		if sys.stdin.isatty():
			print("INPUT ERROR: No input to CyTag was detected, and nor were any arguments passed. Please either send Welsh text to CyTag as standard input, or pass arguments to the program. See the README file for more details on CyTag usage.")
		# Otherwise...
		else:
			# Run the CyTag processing pipeline
			process([sys.stdin.read()])
	# Otherwise...
	else:
		# If the first argument is the word 'evaluate':
		if args[0] == "evaluate":
			# If there are three further arguments, one text argument and two files...
			if len(args) == 4 and os.path.isfile(args[2]) == True and os.path.isfile(args[3]) == True:
				if args[1] != "soft":
					print("ARGUMENT ERROR: 'soft' can be passed as a text flag when evaluating CyTag. Please check that the formatting of the passed arguments is as follows: The correct formatting of arguments is: 'evaluate' 'soft' (optional) GOLD_CORPUS (required) TEST_CORPUS (required)")
				else:
					evaluate("soft", args[2], args[3])
			# Or, if there are two further arguments, and both are files...
			elif len(args) == 3 and os.path.isfile(args[1]) == True and os.path.isfile(args[2]) == True:
				evaluate(None, args[1], args[2])
			# Otherwise...
			else:
				print("ARGUMENT ERROR: Two XML-formatted output files should be passed as arguments in order to evalate CyTag. An optional 'soft' flag can also be passed for a more lenient evaluation. The correct formatting of arguments is: 'evaluate' 'soft' (optional) GOLD_CORPUS (required) TEST_CORPUS (required)")
		# Or, if there was only one argument provided and it was not a file...
		elif len(args) == 1 and os.path.isfile(args[0]) != True:
			# Run the CyTag processing pipeline
			process([args[0]])
		# Otherwise...
		else:
			# Cycle through the arguments and split the input files and the text arguments into separate lists
			input_files, text_args = [], []
			for arg in args:
				input_files.append(arg) if os.path.isfile(arg) else text_args.append(arg)
			# Alert the user if there are no input files among the arguments, or if there are no text arguments
			if len(input_files) == 0 or len(text_args) == 0:
				print("ARGUMENT ERROR: One or more input files, an output filename, and an output format ('tsv', 'xml' or 'all') must be specified. An optional output directory and a specific component to run the pipeline to ('seg', 'sent', 'tok' or 'pos') can also be specified.")
			else:
				# If more than 4 or less than 2 text arguments were passed, alert the user to the correct ordering and formatting for text arguments
				if len(text_args) > 4:
					print("ARGUMENT ERROR: Too many text arguments were given. Text arguments (minimum of 2, maximum of 4) should be: OUTPUT_FILENAME (required) OUTPUT_DIRECTORY (optional) PIPELINE_COMPONENT (optional) OUTPUT_FORMAT (required)")
				elif len(text_args) == 1:
					print("ARGUMENT ERROR: Not enough text arguments were given. Text arguments (minimum of 2, maximum of 4) should be: OUTPUT_FILENAME (required) OUTPUT_DIRECTORY (optional) PIPELINE_COMPONENT (optional) OUTPUT_FORMAT (required)")
				# Otherwise...
				else:
					# If the final text argument is not a valid output format, alert the user to the correct ordering for text arguments
					if text_args[len(text_args)-1] not in ["tsv", "xml", "all"]:
						print("ARGUMENT ERROR: '" + text_args[len(text_args)-1] + "' is not a valid output format. The correct order for text arguments should be: OUTPUT_FILENAME [optional OUTPUT_DIRECTORY, optional PIPELINE_COMPONENT] OUTPUT_FORMAT ('tsv', 'xml' or 'all')")
					# Otherwise...
					else:
						# Take the first text argument as output name, set the directory and component variables to 'None', and take the last text argument as the output format
						output_name, directory, component, output_format = text_args[0], None, None, text_args[len(text_args)-1]
						# If there are two remaining arguments between the required output name and output format...
						if len(text_args[1:-1]) == 2:
							# If the second remaining argument is not a valid pipeline component, alert the user to the correct ordering for text arguments
							if text_args[2] not in ["seg", "sent", "tok", "pos"]:
								print("ARGUMENT ERROR: '" + text_args[2] + "' is not a valid pipeline component. The correct order for 4 text arguments should be: OUTPUT_FILENAME OUTPUT_DIRECTORY PIPELINE_COMPONENT ('seg', 'sent', 'tok' or 'pos') OUTPUT FORMAT")
							# Otherwise, set the first remaining argument as the directory variable and set the second remaining argument as the component variable
							else:
								directory, component = text_args[1], text_args[2]
								# Run the CyTag processing pipeline
								process([input_files, output_name, directory, component, output_format])
						# If there is one remaining argument after the required output name...
						elif len(text_args[1:-1]) == 1:
							# If the remaining argument is in the list of pipeline components, set it as the component variable
							if text_args[1] in ["seg", "sent", "tok", "pos"]:
								component = text_args[1]
							# Otherwise, set it as the directory variable
							else:
								directory = text_args[1] 
							# Run the CyTag processing pipeline
							process([input_files, output_name, directory, component, output_format])
						# Otherwise...
						else:
							# Run the CyTag processing pipeline
							process([input_files, output_name, directory, component, output_format])	