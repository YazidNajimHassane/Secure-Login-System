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
    


@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
