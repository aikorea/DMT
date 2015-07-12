from pymongo import MongoClient

client = MongoClient('localhost', 27017)
client.parcor.authenticate('parcorUser', 'not4share', mechanism='SCRAM-SHA-1')
db = client['parcor']
db.enkr.remove({})
db.counters.update({'_id':'enkr'}, {'$set':{'sequence_value':0}})

