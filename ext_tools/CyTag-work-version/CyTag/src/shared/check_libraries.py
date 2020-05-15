import subprocess

def check_libraries(toolname, tool_tagline, libraries):
	# Find and store the location of pip
	pip_location = subprocess.Popen(["which", "pip"], stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip()
	# Find and store the location of pip3
	pip3_location = subprocess.Popen(["which", "pip3"], stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip()
	# If neither pip nor pip3 are installed...
	if pip_location == "" and pip3_location == "":
		return("\nPIP REQUIRED: Either pip or pip3 is required to check for/install the python libraries needed to run cy_postagger. Please install pip/pip3 before continuing\n")
	# Otherwise...
	else:
		# Set the pip version to use
		pip_version = "pip3" if pip3_location != None else "pip"
		missing_libraries = []
		for library in libraries:
			library_location = subprocess.Popen([pip_version, "show", library], stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
			if library_location == "":
				missing_libraries.append(library)
		if len(missing_libraries) == 0:
			return(None)
		else:
			return("\n{}\n{}\n\nMISSING LIBRARIES: Some of the python libraries {} needed to run cy_postagger are missing. Please install these before continuing (see the README for help)\n".format(tool_tagline, "-"*len(tool_tagline), missing_libraries))

if __name__ == "__main__":
	check_libraries(sys.argv[1:])