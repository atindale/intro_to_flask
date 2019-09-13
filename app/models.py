from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
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

	vehicle_id = db.Column(db.Integer, primary_key=True)
	make_model = db.Column(db.String(45))
	registration = db.Column(db.String(10))

	def __init__(self, make_model, registration):
		self.make_model = make_model.title()
		self.registration = registration.lower()

	def get_id(self):
		return str(self.vehicle_id)

	def add(self, vehicle):
		db.session.add(vehicle)
		return session_commit()

	def update(self):
		return session_commit()

	def delete(self, vehicle):
		db.session.delete(vehicle)
		return session_commit()


class Project(db.Model):
	project_id = db.Column(db.Integer, primary_key=True)
	project_code = db.Column(db.String(10), unique=True)
	project_name = db.Column(db.String(45))
	client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
	client = db.relationship("Client", backref = db.backref('project', lazy='dynamic'))
	project_status_id = db.Column(db.Integer, db.ForeignKey('project_status.project_status_id'))
	status = db.relationship("ProjectStatus", backref = db.backref('project', lazy='dynamic'))

	def __init__(self, project_code, project_name, client, status):
		self.project_code = project_code
		self.project_name = project_name
		self.client = client
		self.status = status

	def add(self, project):
		db.session.add(project)
		return session_commit()

	def update(self):
		return session_commit()

	def delete(self, project):
		db.session.delete(project)
		return session_commit()


class Client(db.Model):
	client_id = db.Column(db.Integer, primary_key = True)
	client_short_name  = db.Column(db.String(55))
	client_name  = db.Column(db.String(255))

	def __init__(self, client_short_name, client_name):
		self.client_short_name = client_short_name
		self.client_name = client_name

	def __repr__(self):
		return self.client_name

	def add(self, client):
		db.session.add(client)
		return session_commit()

	def update(self):
		return session_commit()

	def delete(self, client):
		db.session.delete(client)
		return session_commit()


class ProjectStatus(db.Model):
	project_status_id = db.Column(db.Integer, primary_key = True)
	status  = db.Column(db.String(15))

	def __init__(self, status):
		self.status = status

	def __repr__(self):
		return self.status


class Mileage(db.Model):
	__tablename__ = 'mileage'

	mileage_id = db.Column(db.Integer, primary_key = True)
	journey_date = db.Column(db.Date)
	vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'))
	vehicle = db.relationship("Vehicle", backref = db.backref('mileage', lazy='dynamic'))
	start_km = db.Column(db.Integer)
	end_km = db.Column(db.Integer)
	journey = db.Column(db.String(100))
	client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
	client = db.relationship("Client", backref = db.backref('mileage', lazy='dynamic'))
	project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))
	project = db.relationship("Project", backref = db.backref('project', lazy='dynamic'))
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


# Universal functions

def session_commit():
	try:
		db.session.commit()
	except SQLAlchemyError as e:
		reason = str(e)
		return reason