from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['DMT']
db.parcor.remove({})
db.counters.update({'_id':'parcor'}, {'$set':{'sequence_value':0}})
