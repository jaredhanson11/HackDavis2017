from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hansonj:password@sql.mit.edu/hansonj+'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dkfjalsdj;lfj;lk2j3rlkjl0234923rojkdfldkjfsdlf'
db = SQLAlchemy(app)
api = Api(app)

# Need to import routes after instatiating the api object
import routes
routes.add_resources()
import controllers