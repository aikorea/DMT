from pymongo import MongoClient

def initDB():
    client = MongoClient('localhost', 27017)
    db = client['DMT']
    return db

default_data = {'_id':0, 'data1':"No data", 'lang1':'en', 'data2':"No data", 'lang2':'en', 'src':'none'}

def findOne(db):
    db_res = db.parcor.find_one({})
    ret = db_res
    if ret == None:
        ret = default_data
    return ret

def findAll(db):
    db_res = db.parcor.find({})
    ret = db_res
    if ret == None:
        ret = [default_data]
    return ret

def getNextSeqVal(db):
    seqDoc = db.counters.find_and_modify({'_id':'parcor'}, {'$inc':{'sequence_value':1}}, True)
    return seqDoc['sequence_value']

def insertDB(db, parcors):
    querys = []
    for pc in parcors:
        seqVal = getNextSeqVal(db)
        querys.append({'_id':seqVal, 'data1':pc['data1'], 'lang1':pc['lang1'], 'data2':pc['data2'], 'lang2':pc['lang2'], 'src':pc['src']})
    result = []
    try:
        result = db.parcor.insert(querys)
    except:
        return {'success':-1, 'ids':result}
    return {'success':0, 'ids':result}
