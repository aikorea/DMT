import lib.mydb as mydb
import json
import argparse

parser = argparse.ArgumentParser(description='JSON files uploader')
parser.add_argument('type')
parser.add_argument('query')
parser.add_argument('--output', help='output JSON filename')
args = parser.parse_args()

args.query = json.loads(args.query)

with open('conf.json', 'r') as fd:
    conf = json.load(fd)
db = mydb.init(conf)
res = mydb.find(db, args)

if args.output:
	langs = {"en", "kr"}
	parcors = [{key:value for (key, value) in val.items() if key in langs}\
				for val in res]
	out = {"source":args.query['source'], "type":args.type, "values":parcors}
	with open(args.output, 'w') as fd:
		json.dump(out, fd, indent=2)
else:
	for val in res:
    		print val