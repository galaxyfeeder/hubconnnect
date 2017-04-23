from flask import Flask
from pymongo import MongoClient
from api import tinder
from connector import start as start_nn
import os

# mongo client
client = MongoClient(os.environ.get('MONGODB_URI'))

# flask app
app = Flask(__name__)
app.register_blueprint(tinder.blueprint(client))

# initializing the nnet
start_nn()

# starting flask app
if __name__ == '__main__':
    port = None
    if os.environ.get('PORT'):
        port = int(os.environ.get('PORT'))
    app.run(debug=True, port=port)
