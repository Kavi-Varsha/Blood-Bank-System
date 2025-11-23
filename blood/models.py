from blood import db, login_manager, bcrypt
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    donations = db.relationship('Donation', backref='donor', lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    donation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Donation {self.name} - {self.blood_group}>"


class PatientRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    hospital_name = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<PatientRequest {self.name} - {self.blood_group}>"
