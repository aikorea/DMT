import lib.mydb as mydb
import json
import argparse

parser = argparse.ArgumentParser(description='JSON files uploader')
parser.add_argument('type')
parser.add_argument('query')
args = parser.parse_args()

args.query = json.loads(args.query)

with open('conf.json', 'r') as fd:
    conf = json.load(fd)
db = mydb.init(conf)
res = mydb.find(db, args)
for val in res:
    print val
