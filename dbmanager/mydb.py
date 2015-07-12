from pymongo import MongoClient

def initDB():
    client = MongoClient('localhost', 27017)
    client.parcor.authenticate('parcorUser', 'not4share', mechanism='SCRAM-SHA-1')
    db = client['parcor']
    return db

def findOne(db):
    return db.enkr.find_one({})

def findAll(db):
    return db.enkr.find({})

def getNextSeqVal(db):
    seqDoc = db.counters.find_and_modify({'_id':'enkr'}, {'$inc':{'sequence_value':1}}, True)
    return seqDoc['sequence_value']

def insertDB(db, parcors):
    querys = []
    for parcor in parcors:
        seqVal = getNextSeqVal(db)
        querys.append({'_id':seqVal, 'en':parcor['en'], 'kr':parcor['kr'], 'src':parcor['src']})
    result = []
    try:
        result = db.enkr.insert(querys)
    except:
        return {'success':-1, 'ids':result}
    return {'success':0, 'ids':result}

