from flask import Flask , render_template , request, redirect, session , url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash , generate_password_hash



app= Flask(__name__)

app.config['SECRET_KEY'] = 'my_super_secret_key_123'
#database
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
db = SQLAlchemy(app)

#databasemodel
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(25),unique=True,nullable=False)
    password_hash=db.Column(db.String(150),nullable=False)

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return  check_password_hash(self.password_hash,password)

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login' , methods=["POST"])
def login():
    username=request.form.get('username')
    password=request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username']= username
        return redirect(url_for('dashboard'))
    else :
        return render_template('index.html')


@app.route('/register' , methods=["POST"])
def register():
    username=request.form.get('username')
    password=request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user :
        return render_template("index.html" , error='User already here !')
    else:
        new_user= User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username']=username
        return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template('dashboard.html', username=session['username'])
    redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
