from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from form import userform
#from werkzeug import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/aadarsh/Desktop/AUTISM/database.db'

#file:///home/aadarsh/Desktop/AUTISM/database.db

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/login-example/database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
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
def negative():
    return render_template('/negative.html')

@app.route("/positive.html",methods = ["POST","GET"])
def positive():
    return render_template("positive.html")

@app.route('/qna.html',methods=['GET','POST'])
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
        ID1 = request.form["ID1"]
        ID2 = request.form["ID2"]
        ID3 = request.form["ID3"]
        ID4 = request.form["ID4"]
        ID5 = request.form["ID5"]
        ID6 = request.form["ID6"]
        ID7 = request.form["ID7"]
        ID8 = request.form["ID8"]
        ID9 = request.form["ID9"]
        ID10 = request.form["ID10"]
        ID11 = request.form["ID11"]
        ID12 = request.form["ID12"]
        ID13 = request.form["ID13"]
        ID14 = request.form["ID14"]
        ID15 = request.form["ID15"]
        ID16 = request.form["ID16"]
        ID17 = request.form["ID17"]
        #print("ID1 is", ID1)
            #with sqlite3.connect("database.db") as con:  
            #    cur = con.cursor() 
            #    #cur.execute('DROP TABLE gemscap_table')
            #    cur.execute('''CREATE TABLE IF NOT EXISTS gemscap_table(   
            #    ID1 INTEGER NOT NULL,
            #    ID2 INTEGER NOT NULL,
            #    ID3 INTEGER NOT NULL,
            #    ID4 INTEGER NOT NULL,
            #    ID5 INTEGER NOT NULL,
            #    ID6 INTEGER NOT NULL,
            #    ID7 INTEGER NOT NULL,
            #    ID8 INTEGER NOT NULL,
            #    ID9 INTEGER NOT NULL,
            #    ID10 INTEGER NOT NULL,
            #    ID11 INTEGER NOT NULL,
            #    ID12 INTEGER NOT NULL,
            #    ID13 INTEGER NOT NULL,
            #    ID14 INTEGER NOT NULL,
            #    ID15 INTEGER NOT NULL,
            #    ID16 INTEGER NOT NULL,
            #    ID17 INTEGER NOT NULL,
            #    
            #    ) 
            #    ''') 
            #    cur.execute("INSERT INTO gemscap_table (ID1,ID2,ID3,ID4,ID5,ID6,ID7,ID8,ID9,ID10,ID11,ID12,ID13,ID14,ID15,ID16,ID17) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (ID1,ID2,ID3,ID4,ID5,ID6,ID7,ID8,ID9,ID10,ID11,ID12,ID13,ID14,ID15,ID16,ID17))
            #    con.commit()

        #except:  
        #    con.rollback()  
        #    #msg = "We can not add the employee to the list"  
        #finally:
        return redirect(url_for('positive'))
            #con.close()

    return render_template('qna.html',form = form)

@app.route('/upload')
def uploadfile():
   return render_template('upload.html')
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      print(f)
      f.save(f.filename)
      print(f)
      return 'file uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)