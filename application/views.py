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
    if current_user.is_authenticated:
        return redirect(url_for('new_jot'))
    else:
        return redirect(url_for('login_view'))

@app.route('/myjots')
@login_required
def all_jots():
    user = User.get(id=current_user.id)
    jots = Jot.select().where(Jot.user==user).order_by(Jot.datetime.desc())
    return render_template('all_jots.html', jots=jots)

@app.route('/jotted')
@login_required
def jotted():
    jot = request.args.get('jot')
    return render_template('jotted.html',jot=Jot.get(id=jot))

@app.route('/jot', methods = ['GET', 'POST'])
@login_required
def new_jot():
    form = New_Jot_Form(id=current_user.id)
    if form.validate_on_submit():
        user = User.get(id=int(form.id.data))
        text = form.text.data
        jot =  Jot.create(text=text, user=user)
        return redirect(url_for('jotted',jot=jot.id))

    return render_template("new_jot.html",form=form)

@app.route('/logout', methods=['GET'])
def logout_view():
    logout_user()
    return redirect(url_for('login_view'))

@app.route('/login',methods=['GET','POST'])
def login_view():
    form = Login_Form()
    
    #if they have filled in the form, deal with the login
    if form.validate_on_submit():
        username = form.username.data.lower()#no need for it to be case sensitive
        password = form.password.data

        try:#does the user exist? Redirect to login if they don't
            user = User.get(username=username)
        except User.DoesNotExist:
            flash("User {} does not exist, bro!".format(username))
            return redirect(url_for('login_view'))
        
        #before trying to authenticate, see if the user is confirmed

        if user.confirmed == False:
            flash("User {} is not confirmed - see the link in the email...".format(username))
            return redirect(url_for('login_view'))

        #if they are confirmed, try and authenticate, redirect to login if fails

        if user.authenticate(password):
            #it all works, yay! log them in!
            login_user(user)
            return redirect(url_for('new_jot'))
        else:
            flash("That password isn't right, sis!")
            return redirect(url_for('login_view'))

    #if it's not filled in, or not valid, let them do it again, including errors if needed
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
