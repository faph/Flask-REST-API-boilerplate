from flask import Flask
from flask_restful import Api
from helloworld.routes import routes
import helloworld.config
from helloworld.database import db


app = Flask(__name__)
app.config.from_object(helloworld.config)
db.init_app(app)
api = Api(app)
for route in routes:
    api.add_resource(*route)
