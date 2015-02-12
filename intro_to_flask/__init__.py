from flask import Flask

app = Flask(__name__)

app.secret_key = 'development key'
 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'email_username'
app.config["MAIL_PASSWORD"] = 'email_password'

from routes import mail
mail.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:db_password@db_host/db_name"

from models import db
db.init_app(app)

import intro_to_flask.routes
