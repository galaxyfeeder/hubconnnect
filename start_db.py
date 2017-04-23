from pymongo import MongoClient

client = MongoClient(os.environ.get('MONGODB_URI'))

client.copenhacks.users.insert_one({
    'actual': 'galaxyfeeder',
    'genesis': 'galaxyfeeder',
    'choosed': [],
    'omega': []
})

client.close()
