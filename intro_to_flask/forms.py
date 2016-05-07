from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, StringField
from models import db, User, Client, Project, ProjectStatus
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from validators import Unique

class ContactForm(Form):
	name = TextField("Name", [validators.Required("Please enter your name.")])
	email = TextField("Email", [validators.Required("Please enter your email address."), 
		validators.Email("Please enter a valid email address.")])
	subject = TextField("Subject", [validators.Required("Please enter a subject.")])
	message = TextField("Message", [validators.Required("Please enter a message.")])
	submit = SubmitField("Send")

def enabled_clients():
	return Client.query.all()

def enabled_status():
	return ProjectStatus.query.all()

class ProjectForm(Form):
	project_code = TextField(u'project_code', [validators.Required("Please enter the project code."), 
			Unique(Project, Project.project_code, message='The project code already exists.')])
#	project_code = TextField("project_code", [validators.Required("Please enter your name.")])
	project_name = StringField(u'project_name', [validators.Required()])
	client_name = QuerySelectField(query_factory=enabled_clients, allow_blank=False)
	status = QuerySelectField(query_factory=enabled_status, allow_blank=False)


class SignupForm(Form):
	firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
	lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
	email = TextField("Email",  [validators.Required("Please enter your email address."), 
		validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	submit = SubmitField("Create account")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user:
			self.email.errors.append("That email is already taken")
			return False
		else:
			return True


class SigninForm(Form):
	email = TextField("Email", [validators.Required("Please enter your email address."), 
		validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	submit = SubmitField("Sign In")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append("Invalid e-mail or password")
			return False
