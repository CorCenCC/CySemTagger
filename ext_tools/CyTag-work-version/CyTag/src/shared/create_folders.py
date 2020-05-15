import sys
import os

def create_folders(arguments):
	# If the input is not a list of files or a string, report that there has been an error and stop running
	if isinstance(arguments[0], list) != True and isinstance(arguments[0], str) != True:
		return "INPUT ERROR: The input must either be: a) one or more filenames (if so, an output file name and an optional directory name must also be specified); b) a string of Welsh text"
	# Else, if the first argument is a list of files, then either set the directory to be the same as the output name (second argument) or to use the provided third argument
	elif isinstance(arguments[0], list):
		directory = arguments[1] if arguments[2] == None else arguments[2]
		# If a directory doesn't already exist in the outputs folder, create one
		if not os.path.exists("{}/../../{}/{}".format(os.path.dirname(os.path.abspath(__file__)), "outputs", directory)):
			os.makedirs("{}/../../{}/{}".format(os.path.dirname(os.path.abspath(__file__)), "outputs", directory))
		return None