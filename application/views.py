from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from itsdangerous import TimestampSigner, BadTimeSignature, SignatureExpired
from passlib.hash import pbkdf2_sha256 as hasher

from application import app
from application.forms import Login_Form, New_Jot_Form, New_Password_Form, Forgot_Password_Form
import application.secrets as secrets
from application.models import User, Jot

signer = TimestampSigner(secrets.SECRET_KEY)

@app.route('/')
def index():
    return redirect(url_for('login_view'))

@app.route('/secret')
@login_required
def all_jots():
    users = User.select()
    jots = Jot.select()
    return render_template('all_jots.html',users=users,jots=jots)



@app.route('/jot', methods = ['GET', 'POST'])
@login_required
def new_jot():
    form = New_Jot_Form(id=current_user.id)
    if form.validate_on_submit():
        user = User.get(id=int(form.id.data))
        text = form.text.data
        Jot.create(text=text, user=user)
        flash("You jotted '{}'".format(text))

    return render_template("new_jot.html",form=form)





@app.route('/logout', methods=['GET'])
def logout_view():
    logout_user()
    return redirect(url_for('login_view'))

@app.route('/login',methods=['GET','POST'])
def login_view():
    form = Login_Form()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = User.get(username=username)
        except User.DoesNotExist:
            flash("User {} does not exist, bro!".format(username))
            return redirect(url_for('login_view'))

        if user.authenticate(password):
            login_user(user)
            return redirect(url_for('new_jot'))
        else:
            flash("That password isn't right, sis!")
            return redirect(url_for('login_view'))

    return render_template("login.html",form=form) 



@app.route('/single/<user>/<code>')
def single_use(user, code):
    try:
        signer.unsign(request.url, max_age=3600)
        user_to_login = User.get(username=user)
        login_user(user_to_login)
        return redirect(url_for('new_password'))

    except BadTimeSignature:
        flash("That link was not valid")
        return redirect(url_for('index'))

    except SignatureExpired:
        flash("That link is more than an hour old")
        return redirect(url_for('index'))

@app.route('/password', methods=['GET', 'POST'])
@login_required
def new_password():
    form = New_Password_Form(id=current_user.id)
    if form.validate_on_submit():
        user = User.get(id=int(form.id.data))
        password = form.new_password.data
        user.password_hash = hasher.hash(password)
        user.save()
        flash("Password Changed")
        return redirect(url_for('new_jot'))
    return render_template("new_password.html",form=form)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    form = Forgot_Password_Form()
    if form.validate_on_submit():
        flash("If the address {} is registered with us, then we have sent a login link to it. It is valid for one hour. Use it to change your password.".format(form.email.data))
        try:
            user = User.get(email=form.email.data)
            link_stem = url_for('single_use',user=user.username, code="", _external=True)
            signed_link = signer.sign(link_stem).decode()
            message = "Hi {},\n\nYou requested a login in order to change your password. Please use this link:\n{}\nThanks!\nlove from leadr x".format(user.username,signed_link)
            user.send_email("Forgotten leadr password?",message)
            
        except User.DoesNotExist:
            pass # fail gracefully for security reasons - people now can't tell if an email address is registered on the site
        return redirect(url_for('login_view'))
    return render_template('forgot.html',form=form)
