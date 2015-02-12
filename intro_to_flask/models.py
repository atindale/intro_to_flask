from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))

	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

class Vehicle(db.Model):
	__tablename__ = 'vehicles'

	vehicle_id = db.Column(db.Integer, primary_key = True)
	make_model = db.Column(db.String(45))
	registration = db.Column(db.String(10))

	def __init__(self, make_model, registration):
		self.make_model = make_model.title()
		self.registration = registration.lower()

class Mileage(db.Model):
	__tablename__ = 'mileage'

	mileage_id = db.Column(db.Integer, primary_key = True)
	journey_date = db.Column(db.Date)
	vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.vehicle_id'))
	vehicle = db.relationship("Vehicle", backref = db.backref('mileage', lazy='dynamic'))
	start_km = db.Column(db.Integer)
	end_km = db.Column(db.Integer)
	journey = db.Column(db.String(100))
	client_id = db.Column(db.Integer)
	project_id = db.Column(db.Integer)
	purpose = db.Column(db.String(100))

	def __init__(self, journey_date, vehicle_id, start_km, end_km, journey, client_id, project_id, purpose):
		self.journey_date = journey_date
		self.vehicle_id = vehicle_id
		self.start_km = start_km
		self.end_km = end_km
		self.journey = journey
		self.client_id = client_id
		self.project_id = project_id
		self.purpose = purpose
