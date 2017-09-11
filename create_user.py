from application.models import User
import itsdangerous
import application.secrets as secrets


print("""what is the URL stem?
    1 => wilsonseverywhere.ddns.net:8000
    2 => leadr.freeciv.life
    Something else => use that""")
a = input()
if a == "1":
    URL_STEM = "http://wilsonseverywhere.ddns.net:8000"
elif a == "2":
    URL_STEM = "https://leadr.freeciv.life"
else:
    URL_STEM = a

signer = itsdangerous.Signer(secrets.SECRET_KEY)


username=input('username?')
civname=input('civname?')
email=input('email?')
hexcode=input('hexcode?')

u = User.create(username=username,
        civname=civname,
        email=email,
        confirmed=False,
        hexcode=hexcode)

link_stem = "{}/register/{}/".format(URL_STEM,username)
signed_link = signer.sign(link_stem.encode('utf-8'))



u.send_email("TEST","Testing the registration stuff. Bit of a bind. URL: {} ".format(signed_link.decode()))
