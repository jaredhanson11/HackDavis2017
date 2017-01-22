from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)

# Need to import routes after instatiating the api object
import routes
routes.add_resources()