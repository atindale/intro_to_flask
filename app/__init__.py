from flask import Flask

app = Flask(__name__)

app.config.from_object('config')

from routes import mail
mail.init_app(app)

from models import db
db.init_app(app)

import intro_to_flask.routes