import os # for operating system interfaces
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc

from sqlalchemy.sql import func # func gives you sql functions

#form a path for the database file 
basedir = os.path.abspath(os.path.dirname(__file__)) # get current directory of file app.py and store it into basedir

app = Flask(__name__)
app.app_context().push()

# connect database.db to the current directory 
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' +os.path.join(basedir, 'database.db')
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False # turn on/off tracking modifications of objects, it is off right now

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    hours = db.Column(db.Integer)
    reactiontime = db.Column(db.Integer)

    def __repr__(self): # function to give each database object it's own identity 
        return f'<User {self.name}>'
    
# create route for app and return render template with users query 
@app.route('/') # decorator
def index():
    users = User.query.order_by(asc(User.reactiontime))
    return render_template('index.html', users=users)

@app.route('/<int:user_id>/')  # create route for a certain user
def user(user_id): # return user with a certain id
    user = User.query.get_or_404(user_id)
    return render_template('index.html',user=user)

@app.route('/create/', methods=('GET','POST')) # add a new row/record to the database
def create():
    if request.method == 'POST': # handle the post request to create new record with form info
        name = request.form['name']
        email = request.form['email']
        hours = int(request.form['hours']) # must convert string to int
        reactiontime = int(request.form['reactiontime'])
        user = User(name=name,email=email,hours=hours, reactiontime=reactiontime)
        db.session.add(user) # add the user to database
        db.session.commit() 
        return redirect(url_for('index')) # return user back to main page with leaderboard after receiving the post method after submitting
    return render_template('create.html')
#set up virtual environment by doing(on windows):
#py -m venv env
#env/Scripts/activate

#commands(make sure ur virtual environment is activated):
# export FLASK_APP=app(in linux) OR $Env:Flask_APP='app'(windows powershell)
# py (opens python for window powershell)
# (in python below)
#from app import db, User
# db.create_all()
    
# how to change/add information to the database table
#db.session.add(insert name of User object here) -> makes an insert statement 
#db.session.commit() -> this commits it to the database and assigns an id to the obejct 
# <name of User object>.<data variable> = <insert info here>, then do
    # How to modify existing user object 
        # example) samin.email = example@gmail.com
        # db.session.add(samin)
        # db.session.commit()
    
# query all the records
# User.query.all() -> output is list of user objects

#User.drop_all() -> deletes all items from database

#$Env:Flask_ENV='environment' for debugging 

#HOW TO DISPLAY RECORDS WITH CERTAIN INFORMATION
#User.query.filter_by(name='Samin').all() -> display all User objects of users with name Samin
#User.query.filter_by(name='Samin').first() -> display first user with name 
#User.query.get(3) -> get user with id 3 