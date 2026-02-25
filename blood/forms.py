from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import Length, EqualTo, Email, ValidationError, DataRequired
from blood.models import User
from wtforms.validators import NumberRange

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')
    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email address.')
        
    username=StringField(label='User Name', validators=[Length(min=2,max=40), DataRequired()])
    email_address=StringField(label='Email Id', validators=[Email(), DataRequired()])
    password1=PasswordField(label='Password',validators=[Length(min=6), DataRequired()])
    password2=PasswordField(label='Confirm Password',validators=[EqualTo('password1'), DataRequired()])
    submit=SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username=StringField(label='User Name', validators=[DataRequired()])
    password=PasswordField(label='Password', validators=[DataRequired()])
    submit=SubmitField(label='Sign In')

class DonationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    age = IntegerField('Age',validators=[DataRequired(), NumberRange(min=18, max=65)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired(), Length(min=5)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    blood_group = SelectField('Blood Group', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    submit = SubmitField(label='Submit Donation')

class PatientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    blood_group = SelectField("Blood Group", choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ], validators=[DataRequired()])
    hospital_name = StringField("Hospital Name", validators=[DataRequired()])
    reason = StringField("Reason", validators=[DataRequired()])
    submit = SubmitField("Request Blood")
