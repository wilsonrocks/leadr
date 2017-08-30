from flask import Flask, url_for
from flask_login import LoginManager, current_user

from application.models import User,Jot

app = Flask(__name__)
from application import views


from application import secrets
app.config['SECRET_KEY'] = secrets.SECRET_KEY



login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'login_view'


@login_manager.user_loader
def load_user(user_id_unicode):
    try:
        return User.get(id=int(user_id_unicode))
    except User.DoesNotExist:
        return None

@app.context_processor
def stats():
    total = Jot.select().count()
    if current_user.get_id():
        user = User.get(id=current_user.id)
        user_total = Jot.select().where(Jot.user==user).count()
    else:
        user_total=None
    return dict(
            jot_count=total,
            user_jot_count=user_total)
