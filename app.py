from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from validators.registration_check import CheckUserPassword, CheckUserEmail
from config import DATABASE, SECRET_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123090704Qq@localhost/alex_sql'
app.secret_key = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.secret_key = SECRET_KEY

validator_password = CheckUserPassword()
validator_email = CheckUserEmail()
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)


@app.route('/register', methods=["GET", "POST"])
def registration_handler():
    """Примерная страница регистрации в будущем будет меняться"""
    if request.method == 'GET':
        return render_template("registration.html")
    else:
        login = request.form["email"]
        password = request.form["password"]
        if not validator_email.is_valid_lenght(login):
            flash("Убедитесь , что вы ввели допустимую длину")


        else:
            pswd_hash = generate_password_hash(password)
            if check_password_hash(pswd_hash, password):
                new_user = Users(email=login, password=pswd_hash)
                db.session.add(new_user)
                db.session.commit()
                return render_template("home.html")
    return render_template("registration.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
