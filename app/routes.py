from app import app
from flask import render_template, request, flash, session, url_for, redirect, jsonify
from app.forms import ContactForm, SignupForm, SigninForm, ProjectForm
from flask_mail import Message, Mail
from app.models import db, User, Vehicle, Mileage, Project, Client
from sqlalchemy import extract

mail = Mail()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/link')
def link():
	return render_template('link.html')

def flash_errors(form):
	"""Flashes form errors"""
	for field, errors in form.errors.items():
		for error in errors:
			print(error)
			if error == "This field is required.":
				error_msg = "The %s field is required" % getattr(form, field).label.text
				error_msg
				print(error)
			else:
				error_msg = error
			flash(u"Error in the %s field - %s" % (
				getattr(form, field).label.text,
				error_msg
			), 'danger')

# Example Restful API route

@app.route('/_add_numbers')
def _add_numbers():
	a = request.args.get('a', type=int)
	b = request.args.get('b', type=int)
	return jsonify(result=a + b)

@app.route('/profile')
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signup'))
	else:
		return render_template('profile.html')

##################
#### Vehicles ####
##################

@app.route('/vehicle')
def vehicle_index():
	if 'email' not in session:
		return redirect(url_for('signin'))

	return render_template('vehicle/index.html', vehicles=Vehicle.query.order_by(Vehicle.vehicle_id.desc()).all())

@app.route('/vehicle/add' , methods=['POST', 'GET'])
#@login_required
def vehicle_add():
	if request.method == 'POST':
		make_model = request.form['make_model']
		registration = request.form['registration']
		vehicle = Vehicle(make_model, registration)
		return add(vehicle, vehicle_index, vehicle_add)

	return render_template('/vehicle/add.html')

@app.route('/vehicle/update/<id>', methods=['POST', 'GET'])
#@login_required
def vehicle_update(id):
	# Get vehicle by primary key
	vehicle = Vehicle.query.get_or_404(id)
	if request.method == 'POST':
		vehicle.make_model = request.form['make_model']
		vehicle.registration = request.form['registration']
		return update(vehicle, vehicle_index, vehicle_update, id)

	return render_template('/vehicle/update.html', vehicle=vehicle)

@app.route('/vehicle/delete/<id>', methods=['POST', 'GET'])
#@login_required
def vehicle_delete(id):
		vehicle = Vehicle.query.get_or_404(id)
		return delete(vehicle, vehicle_index)

#################
#### Project ####
#################

@app.route('/project')
def project_index():
	if 'email' not in session:
		return redirect(url_for('signin'))
	projects = Project.query.order_by(Project.project_code)
	return render_template('project/index.html', projects=projects)

@app.route('/project/add', methods=['POST', 'GET'])
def project_add():
	form = ProjectForm()

	if form.validate_on_submit():
		project = Project(project_code=form.project_code.data, 
		                  project_name=form.project_name.data,
						  client=form.client_name.data, 
						  status=form.status.data)
		db.session.add(project)
		db.session.commit()
		flash('Your project has been added.')
		return redirect(url_for('project_index'))
	else:
		flash_errors(form)

	# projects = Project.query.all()
	return render_template('project/add.html', form=form)

#	if request.method == 'POST':
#		project_code = request.form['project_code']
#		project_name = request.form['project_name']
#		client = request.form['client']
#		project_status = request.form['project_status']
#		project = Project(project_code, project_name, client, project_status)
#		return add(project, project_index, project_add)

#	return render_template('project/add.html',)

@app.route('/project/update/<id>', methods=['POST', 'GET'])
def project_update(id):

	project = Project.query.get_or_404(id)
	form = ProjectForm(obj=project)

	if form.validate_on_submit():
		print("in validate_on_submit")
		project = Project(project_code=form.project_code.data, project_name=form.project_name.data, client=form.client_name.data, status=form.status.data)
		db.session.commit()
		flash('Your project has been added.')
		return redirect(url_for('project_index'))

	return render_template('project/update.html', form=form)

@app.route('/project/delete/<id>', methods=['POST', 'GET'])
def project_delete(id):
	project = Project.query.get_or_404(id)
	return delete(project, project_index)

#################
#### Clients ####
#################

@app.route('/client')
def client_index():
	if 'email' not in session:
		return redirect(url_for('signin'))

	clients = Client.query.order_by(Client.client_name)

	return render_template('client/index.html', clients=clients)

@app.route('/client/add', methods=['POST', 'GET'])
#@login_required
def client_add():
	if request.method == 'POST':
		client_short_name = request.form['client_short_name']
		client_name = request.form['client_name']
		client = Client(client_short_name, client_name)
		return add(client, client_index, client_add)

	return render_template('/client/add.html')

@app.route('/client/update/<id>', methods=['POST', 'GET'])
#@login_required
def client_update(id):
	# Get client by primary key
	client = Client.query.get_or_404(id)
	if request.method == 'POST':
		client.client_short_name = request.form['client_short_name']
		client.client_name = request.form['client_name']
		return update(client, client_index, client_update, id)

	return render_template('/client/update.html', client=client)

@app.route('/client/delete/<id>', methods=['POST', 'GET'])
#@login_required
def client_delete(id):
		client = Client.query.get_or_404(id)
		return delete(client, client_index)

#################
#### Mileage ####
#################

@app.route('/mileage')
@app.route('/mileage/<int:this_year>')
def show_mileage(this_year=None):
	if 'email' not in session:
		return redirect(url_for('signin'))
	if this_year == None:
		mileage = Mileage.query.order_by(Mileage.journey_date.desc()).limit(15)
	else:
		mileage = Mileage.query.filter(extract('year', Mileage.journey_date) == this_year)
#		mileage = Mileage.query.filter_by(Mileage.journey_date.year == year)

	return render_template('mileage/index.html', mileage=mileage)

#######################
#### Sign-up forms ####
#######################

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	if 'email' in session:
		return redirect(url_for('profile'))

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email

			return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('signup.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()

	if 'email' in session:
		return redirect(url_for('profile'))

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signin.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('signin.html', form=form)


@app.route('/signout')
def signout():
	if 'email' not in session:
		return redirect(url_for('signin'))

	session.pop('email', None)
	return redirect(url_for('home'))

#
# CRUD FUNCTIONS
# Arguments  are data to add, function to redirect to if the add was successful and if not
#

def add(data, func1, func2):
    add = data.add(data)
    #if does not return any error
    if not add :
       flash("Add was successful")
       return redirect(url_for(str(func1.__name__)))
    else:
       message=add
       flash(message)
       return redirect(url_for(str(func2.__name__)))


def update(data, func1, func2, id):
	update = data.update()
	# if does not return any error
	if not update:
		flash("Update was successful")
		return redirect(url_for(str(func1.__name__)))
	else:
		message = update
		flash(message)
		return redirect(url_for(str(func2.__name__), id=id))


def delete(data, func1):
	delete = data.delete(data)
	if not delete:
		flash("Delete was successful")
	else:
		message = delete
		flash(message)
	return redirect(url_for(str(func1.__name__)))
