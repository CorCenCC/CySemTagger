#!usr/bin/env python3
#-*- coding: utf-8 -*-
"""
'cy_textsegmenter.py'

A text segmenter for Welsh texts.

Accepts as arguments:
	--- REQUIRED: A string of Welsh language text.
	or:
	--- REQUIRED: One or more Welsh input text files (raw text).

Returns:
	--- cy_taggedobject with text segmented

Developed at Cardiff University as part of the CorCenCC project (www.corcencc.org).

2016-2017 Steve Neale <steveneale3000@gmail.com, NealeS2@cardiff.ac.uk>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses>.
"""

import sys
import os

from cy_taggedobject import taggedobject
from shared.create_folders import *
from shared.get_lines import *

def segment_text(input_data, output):
	# Split the input data into lines
	lines = get_lines(input_data)
	# Store the lines in the output object as segments
	output.store_segments(lines)
	# Return the output object
	return(output)

if __name__ == "__main__":
	args = sys.argv[1:]
	# If there was only one argument provided and it was not a file...
	if len(args) == 1 and os.path.isfile(args[0]) != True:
		# Run the text segmenter treating the argument as a single string of text
		segment_text(args[0], taggedobject())
	#Otherwise:
	else:
		# Run the text segmenter treating the arguments as input files
		segment_text(args, taggedobject())