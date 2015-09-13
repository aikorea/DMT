import lib.mydb as mydb
import json
import argparse

parser = argparse.ArgumentParser(description='JSON files uploader')
parser.add_argument('type', help='type of corpus(sentence/?/?)')
parser.add_argument('--langs', help='language list (delimiter "-")')
parser.add_argument('--source', help='DB source')
parser.add_argument('--query', help='manual query')
parser.add_argument('--output', help='output JSON filename')
args = parser.parse_args()

# initialize DB connection
with open('conf.json', 'r') as fd:
    conf = json.load(fd)
db = mydb.init(conf)

# set query and find
if args.query:
	query = json.loads(args.query)
else:
	query = dict()
	if args.langs:
		langs = args.langs.split("-")	
		for lang in langs:
			query[lang] = {"$exists" : True}
	if args.source:
		query['source'] = args.source

res = mydb.find(db, args.type, query)

# output
if args.output:
	out = dict();
	out["type"] = args.type
	
	langs = {"en", "kr", "jp", "ch", "fr"}
	parcors = [{key:value for (key, value) in val.items() if key in langs}\
				for val in res]
	out["values"] = parcors
	
	if "source" in query:
		out["source"] = query["source"]
	
	with open(args.output, 'w') as fd:
		json.dump(out, fd, indent=2)
else:
	for val in res:
		print val
