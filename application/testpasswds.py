from .models import User

while True:
    uname = input("Username?")
    passwd = input("Pasword")
    print("match={}".format(User.get(username=uname).authenticate(passwd)))
