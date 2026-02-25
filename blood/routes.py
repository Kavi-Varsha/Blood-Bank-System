from blood import app, db
from flask import render_template, redirect, url_for, flash, request
from blood.models import User, Donation
from blood.forms import RegisterForm, LoginForm, DonationForm
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from flask import abort

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "Admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
from datetime import datetime
from blood.forms import PatientForm 
from datetime import timedelta
from blood.models import PatientRequest


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    donations = Donation.query.filter_by(donor_id=current_user.id).all()
    return render_template('dashboard.html', donations=donations)


# Admin Dashboard Route
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    pending_donations = Donation.query.filter_by(status="Pending").all()
    open_requests = PatientRequest.query.filter_by(status="Open").all()
    return render_template(
        'admin_dashboard.html',
        donations=pending_donations,
        requests=open_requests
    )


# Admin Actions
@app.route('/admin/approve_donation/<int:donation_id>', methods=['POST'])
@login_required
@admin_required
def approve_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    donation.status = "Approved"
    db.session.commit()
    flash("Donation approved.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject_donation/<int:donation_id>', methods=['POST'])
@login_required
@admin_required
def reject_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    donation.status = "Rejected"
    db.session.commit()
    flash("Donation rejected.", "danger")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/fulfill_request/<int:request_id>', methods=['POST'])
@login_required
@admin_required
def fulfill_request(request_id):
    request_entry = PatientRequest.query.get_or_404(request_id)
    request_entry.status = "Fulfilled"
    db.session.commit()
    flash("Request fulfilled.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/request/<int:request_id>/cancel', methods=['POST'])
@login_required
@admin_required
def cancel_request(request_id):
    req = PatientRequest.query.get_or_404(request_id)
    req.status = "Canceled"
    db.session.commit()
    flash("Patient request canceled.", "warning")
    return redirect(url_for('admin_dashboard'))


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
        # Add eligibility check
        last_donation = Donation.query.filter_by(
            donor_id=current_user.id
        ).order_by(Donation.donation_date.desc()).first()

        if last_donation:
            days_since = (datetime.utcnow() - last_donation.donation_date).days
            if days_since < 90:
                flash(
                    f"You are not eligible to donate yet. Please wait {90 - days_since} more days.",
                    category="danger"
                )
                return redirect(url_for('donation_page'))
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
    form = PatientForm()
    if form.validate_on_submit():
        request_entry = PatientRequest(
            name=form.name.data,
            age=form.age.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            blood_group=form.blood_group.data,
            hospital_name=form.hospital_name.data,
            reason=form.reason.data
        )
        db.session.add(request_entry)
        db.session.commit()

        flash("Blood request submitted successfully!", category='success')
        return redirect(url_for('home_page'))

    return render_template('patient.html', form=form)


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
