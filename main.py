from flask import Flask , render_template , request, redirect, session , url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash , generate_password_hash



app= Flask(__name__)

#database
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
db = SQLAlchemy(app)

#databasemodel
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(25),unique=True,nullable=False)
    password=db.Column(db.String(150),nullable=False)

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
    username=request.form['username']
    password=request.form['password']
    username=request.form['username'] 
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username']= username
        return redirect(url_for('dashboard'))
    else :
        return render_template('index.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
