from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_sqlalchemy  import SQLAlchemy
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from form import userform, health
import os
from werkzeug.utils import secure_filename
from Emotion_Recognition import model

UPLOAD_FOLDER = 'C:\\Users\\aadar\\Desktop\\AUTISM'                     #Aadarsh Path

ALLOWED_EXTENSIONS = {'mov', 'MOV'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\aadar\\Desktop\\AUTISM\\database.db'                  #Aadarsh Path


#file:///home/aadarsh/Desktop/AUTISM/database.db

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/login-example/database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
 
global username
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    username= db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('confirm password', validators=[InputRequired(), EqualTo('password')])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    str = ""
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        global username
        username=user.username
        print(username)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        str = "Invalid Username or Password"
        #return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form, str = str)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    
    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            #print("EXISTS")
            return render_template('signup.html', form=form, str="Username is taken, try another")        
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        #return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/negative.html',methods=['GET','POST'])
@login_required
def negative():
    return render_template('/negative.html')

@app.route("/positive.html",methods = ["POST","GET"])
@login_required
def positive():
    return render_template("positive.html")

@app.route('/qna.html',methods=['GET','POST'])
@login_required
def userprofile():
    
    form = userform()
    #print("form.errors is ", form.errors )
    #if form.is_submitted():
        #print("++++submitted+++")
    #if not form.validate():
        #print("++++invalid++++")
    #print("form.errors2 is ", form.errors )
    
    if form.validate_on_submit():
        result = request.form
        #print(result)
        ## save in database here itself
        #try:
        AGE = request.form['AGE']
        ID1 = request.form["ID1"]
        ID2 = request.form["ID2"]
        ID3 = request.form["ID3"]
        ID4 = request.form["ID4"]
        ID5 = request.form["ID5"]
        
        with sqlite3.connect("database.db") as con:  
                cur = con.cursor() 
                #cur.execute('DROP TABLE AUTISM')
                cur.execute('''CREATE TABLE IF NOT EXISTS AUTISM(   
                USERNAME STRING PRIMARY KEY,
                AGE STRING,
                ID1 INTEGER,
                ID2 INTEGER,
                ID3 INTEGER,
                ID4 INTEGER,
                ID5 INTEGER,
                ANGRYCOUNT INTEGER,
                DISGUSTCOUNT INTEGER,
                FEARCOUNT INTEGER,
                HAPPYCOUNT INTEGER,
                SADCOUNT INTEGER,
                SURPRISECOUNT INTEGER,
                NEUTRALCOUNT INTEGER
                
                ) 
                ''') 
                global username
                cur.execute("INSERT INTO AUTISM (USERNAME,AGE,ID1,ID2,ID3,ID4,ID5) VALUES (?,?,?,?,?,?,?)", (username,AGE,ID1,ID2,ID3,ID4,ID5))
                cur.execute("INSERT INTO DATABASE (USERNAME) VALUES(?)",(username,) )
                con.commit()
                
                return redirect(url_for('dashboard'))
                con.close()
                
    return render_template('qna.html',form = form)

@app.route('/upload')
@login_required
def uploadfile():
   return render_template('upload.html')


	
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(file.filename)
            global username
            print(username)
            model(file.filename,username)
            #function call for model 1 and parameter is file.filename
            return redirect(url_for('dashboard', filename=filename))
    return render_template('dashboard.html')

@app.route('/temperature', methods=['GET', 'POST'])
def temp():
    form = health()
    if form.is_submitted():
        result = request.form

        TEMPERATURE = result['TEMPERATURE']
        HEARTRATE = result['HEARTRATE']
        print(TEMPERATURE, HEARTRATE)
        global username
        with sqlite3.connect("database.db") as con:  
                cur = con.cursor() 
                #cur.execute('DROP TABLE AUTISM')
                cur.execute(''' UPDATE AUTISM SET TEMPERATURE = {}, HEARTRATE = {} WHERE USERNAME = "{}" 
                '''
                .format(TEMPERATURE, HEARTRATE, str(username))) 
                
                con.commit()
                
                return redirect(url_for('dashboard'))
                #con.close()
        

    return render_template('temperature.html', form = form)



if __name__ == '__main__':
    app.run(debug=True)