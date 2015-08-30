from pymongo import MongoClient

def init(conf):
    client = MongoClient(conf['host'],conf['port'])
    db = client['DMT']
    db.authenticate(conf['id'],conf['pwd'])
    return db

def find(db, args):
    if args.type == 'sentence':
        collection = db.sentence
    else:
        return None
    res = collection.find(args.query)
    return res

def insert(db, data):
    if data['type'] == 'sentence':
        collection = db.sentence
    else:
        return None

    additional_info = {}
    if 'source' in data:
        additional_info['source'] = data['source']
    for value in data['values']:
        value.update(additional_info)

    result = collection.insert(data['values'])
    return result
