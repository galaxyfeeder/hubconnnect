from pymongo import MongoClient

client = MongoClient()

client.copenhacks.users.insert_one({
    'actual': 'galaxyfeeder',
    'genesis': 'galaxyfeeder',
    'choosed': [],
    'omega': []
})

client.close()
