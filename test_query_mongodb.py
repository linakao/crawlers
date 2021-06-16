import pprint
from pymongo import MongoClient

client = MongoClient()
db = client.pchome
coll = db.products

# name contains panasonic
name_condition = {'name': {'$regex': '.*Panasonic.*', '$options': 'i'}}
# data = coll.find(name_condition)

# comparison operator
price_condition = {'price': {'$gte': 10000}}
# data = coll.find(price_condition)

# and operator example
# data = coll.find({'$and': [name_condition, price_condition]})

# for d in data:
#     print(d['name'], d['price'])

# update example
# coll.update_one({'name': 'Panasonic 國際牌30L蒸氣烘烤微波爐(NN-BS1700)'}, {'$set': {'price': 30000}})

# upsert example, insert if not exist
# coll.update_one({'name': 'Puca'}, {'$set': {'name': 'Puca', 'price': 999999999}}, upsert=True)

# delete example
coll.delete_one({'name': 'Puca'})