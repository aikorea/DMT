# -*- coding: utf-8 -*-

import argparse
import json

parser = argparse.ArgumentParser(description='Plain Text to JSON')
parser.add_argument('file1', help='input plain text')
parser.add_argument('file2', help='output JSON file')
parser.add_argument('source', help='source name')
parser.add_argument('--type', help='type of corpus(defalut:"sentence")')
parser.add_argument('--langs', help='language order of input lines(default:"kr-en"')
args = parser.parse_args()

# parsing the language order
if not args.langs:
	langs = ["kr", "en"]
else:
	langs = args.langs.split("-")

# read the input text in the order of langs
parcors = []
with open(args.file1, 'r') as fd:
	while True:
		parcor = dict()
		for lang in langs:
			line = fd.readline().strip()
			if not line:
				break
			parcor[lang] = line
		if len(langs) != len(parcor):
			break
		else:
			parcors.append(parcor)

# generate output file
data = dict()
data['source'] = args.source
if args.type:
	data['type'] = args.type
else:
	data['type'] = 'sentence'
data['values'] = parcors

with open(args.file2, 'w') as fd:
	json.dump(data, fd, indent=2)