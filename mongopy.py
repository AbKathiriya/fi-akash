import pymongo
import json
from bson import json_util
from bson.objectid import ObjectId

if __name__ == '__main__':
    # Connection to Mongo DB
    try:
        conn=pymongo.MongoClient('localhost', 27017)
        print "Connected successfully!!!"
    except pymongo.errors.ConnectionFailure, e:
       print "Could not connect to MongoDB: %s" % e

    # Select database
    db = conn.mydb

    # Select collection
    collection = db.Users

    # find documents
    docs = collection.find()
    for doc in docs:
        print json_util.dumps(doc, indent=4)

    # Insert one document
    doc = {'name':'Sue','age':'22','gender':'female','stream':'IT'}
    collection.insert_one(doc)

    # Update the documents
    # 1. This will update the whole document
    collection.update({"_id":ObjectId('58a990f713e4367839a0243c')},{"age":"25"})
    doc = collection.find_one({'_id':ObjectId('58a990f713e4367839a0243c')})

    # 2. Update using $set operator
    collection.update({"_id":ObjectId('58abb6a586e76105aea02ee1')},{"$set":{"age":"25"}})

    # Get the Users collection stats
    print json.dumps(db.command({'collstats': 'Users'}), indent = 4)
