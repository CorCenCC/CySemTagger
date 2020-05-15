#!usr/bin/env python3
#-*- coding: utf-8 -*-
"""
'cy_contractionprefix_extractor.py'

Extract an up-to-date CorCenCC dictionary of contractions and prefixes, for use with CyTag.

Accepts as arguments:
	--- REQUIRED:
	--- OPTIONAL:

Developed at Cardiff University as part of the CorCenCC project (www.corcencc.org).

2017 Steve Neale <steveneale3000@gmail.com, NealeS2@cardiff.ac.uk>
"""

from __future__ import print_function
import httplib2
import os

import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-extract_contractionsprefixes.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'CorCenCC Contraction and Prefix Extractor'

def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-extract_contractionsprefixes.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

def extract_contractionsprefixes():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')

	service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

	spreadsheetId = "1ufx1fB8LNI7bMv07Zyji8DE8jGCsW2bpRifEMBWVILg"

	rangeName = "Sheet1!A1:K"

	result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()

	contractionprefix_dict = {}

	for i, entry in enumerate(result["values"]):
		if len(entry) > 0:
			full_forms = []
			for full_form in entry[2:]:
				if full_form != "":
					full_forms.append(full_form)
			contractionprefix_dict[entry[0][1:]] = [entry[1], full_forms]
	
	print(contractionprefix_dict)
	output = open("contractions_and_prefixes.json", "w")
	json.dump(contractionprefix_dict, output)

if __name__ == '__main__':
	extract_contractionsprefixes()    