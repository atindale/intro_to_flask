from flask import Flask

app = Flask(__name__)

app.config.from_object('config')

from app import routes

from app.routes import mail
mail.init_app(app)

from app.models import db
db.init_app(app)
