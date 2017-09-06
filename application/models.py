from peewee import Model, CharField, DateTimeField, TextField, ForeignKeyField, PostgresqlDatabase
from passlib.hash import pbkdf2_sha256 as hasher

from datetime import datetime
from email.message import EmailMessage
import smtplib

from . import secrets

db = PostgresqlDatabase(secrets.POSTGRES_DB,
        user=secrets.POSTGRES_USER,
        password=secrets.POSTGRES_PASSWORD,
        host='127.0.0.1')

class User(Model):
    class Meta:
        database = db
        db_table = "user_account"
    pass
    
    username = CharField()
    civname = CharField()
    email = CharField(verbose_name="Email Address")
    hexcode = CharField(max_length=6)
    password_hash = CharField(max_length=87)
    avatar = CharField(max_length=255, null=True)

    #flask-login stuff
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False


    def get_id(self):
        return str(self.id)

    def authenticate(self, password):
        return hasher.verify(password,self.password_hash)

    def send_email(self,subject,text):
        """Sends email with subject *subject* and body *text* to the user's email address."""
        message = EmailMessage()
        message['From'] = secrets.FROM_ADDR
        message['To'] = self.email
        message['Subject'] = subject
        message.set_content(text)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(secrets.FROM_ADDR, secrets.EMAIL_PASSWORD)
        server.send_message(message)



class Jot(Model):
    class Meta:
        database = db
    user = ForeignKeyField(User, related_name='jots')
    datetime = DateTimeField(default=datetime.now)
    text = CharField(max_length=140)

    def date_formatted(self):
        return self.datetime.strftime("%d %b %y")
    def time_formatted(self):
        return self.datetime.strftime("%H:%M")

#TODO Add model for a turn, fields: timestamp, year, turn no
