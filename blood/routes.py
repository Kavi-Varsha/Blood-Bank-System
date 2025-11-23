from blood import app, db
from flask import render_template, redirect, url_for, flash, request
from blood.models import User, Donation
from blood.forms import RegisterForm, LoginForm, DonationForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from blood.forms import PatientForm 

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/donate', methods=['GET', 'POST'])
@login_required
def donation_page():
    form = DonationForm()
    if form.validate_on_submit():
        donation = Donation(
            name=form.name.data,
            age=form.age.data,
            email=form.email.data,
            address=form.address.data,
            phone_number=form.phone_number.data,
            blood_group=form.blood_group.data,
            gender=form.gender.data,
            donation_date=datetime.utcnow(),     # ✅ set donation_date
            donor_id=current_user.id             # ✅ set donor_id
        )
        db.session.add(donation)
        db.session.commit()
        flash("Donation successfully recorded!", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:  
        for field, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error with {field}: {err_msg}', category='danger')
    return render_template('donation.html', form=form)

@app.route('/patient', methods=['GET', 'POST'])

def patient_page():
    form = PatientForm()  # ✅ create the form instance
    if form.validate_on_submit():
        # Process form data here if needed
        flash("Form submitted successfully!", category='success')
        return redirect(url_for('home_page'))

    return render_template('patient.html', form=form)  # ✅ pass form to template

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_page'))
        else:
            flash('Username and password do not match! Please try again.', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out.", category='info')
    return redirect(url_for("home_page"))
