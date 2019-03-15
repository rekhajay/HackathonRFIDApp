from app import db
from app.forms import RegistrationForm
from flask import  render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from app.models import Swipe
from app.models import Rfid
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.forms import SimulateSwipeForm
from app.forms import CreateRFIDForm
from app.forms import RfidAssignForm

#import RPi.GPIO as GPIO

#ajax
from flask import request, jsonify

#Notes
#AMke sure you import the new models
#make sure you import the new Forms


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


    
@app.route('/posts')
@login_required
def posts():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('posts.html', title='Posts', user=user, posts=posts)
class UserSwipe():
  def __init__(self,username='',time=''):
    self.username = username
    self.time=time


@app.route('/monitorSwipes')
@login_required
def monitorSwipes():
    user = {'username': 'Miguel'}
  #  swipes = [
  #      {
  #          'entry': {'username': 'John'},
  #          'time': 'Monday Jan 1st:  2 AM'
  #      },
  #     {
  #          'entry': {'username': 'Sephan'},
  #          'time': 'Tuesday Jan 2nd: 5 PM'
  #      }
  #  ]
    #read the swipes form the database
    #for each swipe get the userid that corresponds to the RFID
    #create the swipes json

    #swipesList = swipe.query.join(userrfid, swipe.rfid==userrfid.rfid).add_columns(swipe.timestamp, swipe.user_id,  userrfid.userId).
    userswipes= []
    swipesList = Swipe.query.all()
    for curswipe in swipesList:
      rfid = Rfid.query.filter_by(rftagid=curswipe.rfid).first()
      # usswp=UserSwipe('hi','12/12/1969')
      # userswipes.append(usswp)
      if rfid is not None:
        user = User.query.filter_by(id=rfid.user_id).first()
        usswp=UserSwipe(user.username, curswipe.time)
        #usswp=UserSwipe('hi', '12/12/1969')
        userswipes.append(usswp)
    
    return render_template('swipes.html', title='Swipes', user=user, swipes=swipesList, userswipes=userswipes)


@app.route('/assignRFIDs', methods=['GET', 'POST'])
def assignRFIDs():
    form = RfidAssignForm()
    if form.validate_on_submit():
        #create a row in rfiduser table, or just create a username column in rfid tavle
        #NOTE: we are passing in users = (this is the db.relationship field)
        rfidassignment = Rfid(rftagid=form.rfid.data, users=form.user_list.data)
        db.session.add(rfidassignment)
        db.session.commit()
        flash('Your assignment has been recorded!')
        return redirect(url_for('index'))
    return render_template('assignRFID.html', title='Assign RFID to User', form=form)



#@app.route('/userHasSwiped')
#def createUserSwipeEntry():
    # TODO :: This api will be triggered on an User Swipe Event
    # It will get the RFID from the User Swipe Event and map the RFID to the assigned user ID
    # It will save the event with the date and user id to the swipe table in the database
  
    #rfid = from event
    #userid = get_userid_for_rfid()

@app.route('/simulateSwipe', methods=['GET', 'POST'])
def simulateSwipe():
    form = SimulateSwipeForm()
    if form.validate_on_submit():
        #future map the rfid to the userid using the table mapping
        #user = User.query.filter_by(username=current_user.username).first()
        rfid = Rfid.query.filter_by(rftagid=form.rfid.data).first()
        #swipe = Swipe(timestamp=form.time.data, user_id=rfid.user_id)
        swipe = Swipe (time=form.time.data, rfid=form.rfid.data)

        db.session.add(swipe)
        db.session.commit()
        flash('Your swipe has been recorded!')
        return redirect(url_for('index'))
    return render_template('simulateSwipe.html', title='Simulate Swipe', form=form)



@app.route('/startstopled')
def dashboard():
    return render_template('startstopLED.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/createnewrfid', methods=['GET', 'POST'])
def createnewrfid():
    form = CreateRFIDForm()
    if form.validate_on_submit():
        rfid = Rfid(rftagid=form.rftagid.data, users=form.user_list.data)
        db.session.add(rfid)
        db.session.commit()
        flash('Congratulations, you have added a new RFID!')
        return redirect(url_for('login'))
    return render_template('createrfid.html', title='Create RFID', form=form)

@app.route('/api/startblinking', methods=['POST'])
def startblinking():
   # json = request.get_json()
   # first_name = json['first_name']
   # last_name = json['last_name']

   # GPIO.setup(4, GPIO.OUT)
   # GPIO.output(4,False)
   # for x in range (1,10):
   #     GPIO.output (4, True)
   #     time.sleep (1)
   #     GPIO.output (4, False)
   #     time.sleep(1)

    return jsonify(first_name='Started', last_name='Biinking')


@app.route('/api/stopblinking', methods=['POST'])
def stopblinking():
   # json = request.get_json()
   # first_name = json['first_name']
   # last_name = json['last_name']

    #GPIO.setup(4, GPIO.OUT)
    #GPIO.output(4,False)

    return jsonify(first_name='Stopped', last_name='Blinking')
