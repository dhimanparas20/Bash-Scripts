import pymongo
import random
import string 
from passlib.hash import pbkdf2_sha256
DEFAULT_STRING= "mongodb://localhost:27017/"
#Syntax for cloud based Connection String
'''client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster1.n5hitou.mongodb.net/?retryWrites=true&w=majority")'''

def hashit(data:str):  #hashes any data givent to it
        # Hash the password using Passlib's pbkdf2_sha256
        return pbkdf2_sha256.hash(data)
def verifyHash(password:str, hashedpassword:str):
        return pbkdf2_sha256.verify(password, hashedpassword)
def genString(length=15):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
class MongoDB:  #Main Class
    def __init__(self,db_name=None,collection_name=None,connectionStr=DEFAULT_STRING):
        try: 
            self.client = pymongo.MongoClient(connectionStr)
            if db_name and collection_name:
                self.db = self.client[db_name]
                self.collection = self.db[collection_name]
        except:
            return False       
    def addDB(self,db_name,collection_name):
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]  
    def getAllDB(self):
        database_list = self.client.list_database_names()
        result = []
        for database in database_list:
            result.append(database) 
        return result 
    def getAllCollection(self,db_name=None):
        if db_name:
            db = self.client[db_name]
        else:
            db = self.client[self.db]    
        collections = db.list_collection_names()
        result = []
        for collection in collections:
            result.append(collection) 
        return result   
    def insert(self, data={}):
        self.collection.insert_one(data)
        #lst = [data]
        #self.collection.insert_many(lst)
        return True
    def fetch(self, data=None, show_id=False):
        result = []
        projection = {"_id": 0} if show_id==False else {}
        res = self.collection.find(data, projection)
        for item in res:
            if show_id and "_id" in item:
                # Convert _id to string format if show_id is True
                item["_id"] = str(item["_id"])

            result.append(item)
        print('======================================')
        print(result)
        return result   
    def count(self,data={}):
        count = self.collection.count_documents(data)
        return count  
    def update(self,prev,nxt):
        nxt = {"$set":nxt}
        up = self.collection.update_many(prev,nxt)
        count  = up.modified_count
        if count >0:
            return True
        elif count == 0:
            return ({"message":"Nothing To modify"})
        else:
            return False        
    def delete(self,data={}):
        dlt = self.collection.delete_many(data)
        count = dlt.deleted_count
        if count > 0:
            return True
        else:
            return False  
    def dropDB(self,db_name=None):
        try:
            if db_name:
                self.client.drop_database(db_name)
            else:
                if self.db:
                    self.client.drop_database(self.db) 
                else:
                    return False          
            return True
        except Exception as e:
            # print(f"Error: {e}")
            return False
    def dropCollection(self,db_name=None,collection_name=None): #Delete A Collection
        try:
            if collection_name and db_name==None:
                db = self.client[self.db]
                db.drop_collection(collection_name)    
                
            if db_name and collection_name:
                db = self.client[db_name]
                db.drop_collection(collection_name)
                    
            return True
        except Exception as e:
            # print(f"Error: {e}")
            return False               
    def close(self):
        self.client.close()

#USAGE EG.
'''
from pyMongo import MongoDB
mydb = MongoDB("db_name","doc_name")
hasedpass = MongoDB.hashit("mypassword")
data = {"name":"d","id":4,"tax":False,"password":hashedpass}
mydb.insert(data)
mydb.fetch()
data = mydb.fetch({"name":"d"})
hashpass = data[0]["password"]
print(mydb.verifyHash("mypassword",hashpass))
'''       