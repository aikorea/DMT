import lib.mydb as mydb
import argparse
import json

parser = argparse.ArgumentParser(description='JSON files uploader')
parser.add_argument('files', nargs='+')
args = parser.parse_args()

with open('conf.json', 'r') as fd:
    conf = json.load(fd)

db = mydb.init(conf)
for file_path in args.files:
    with open(file_path, 'r') as fd:
        data = json.load(fd)
    mydb.insert(db, data)
