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
    URL_STEM = "http://leadr.freeciv.life"
else:
    URL_STEM = a

signer = itsdangerous.Signer(secrets.SECRET_KEY)


username=input('username?')
civname=input('civ leader name?')
email=input('email?')
hexcode=input('hexcode?')
peoplename=input('name of your civilisation?')

u = User.create(username=username,
        civname=civname,
        email=email,
        confirmed=False,
        hexcode=hexcode,
        avatar='avatar/{}-large.png'.format(peoplename))

link_stem = "{}/register/{}/".format(URL_STEM,username)
signed_link = signer.sign(link_stem.encode('utf-8'))



u.send_email("Welcome to Leadr!","""
Howdy {}!

Welcome to Leadr. This is an experimental 'secret microblog' - you may be part of the birth of the newest social media craze.
Of course you may not be.

The idea is that you 'jot' your thoughts down through the site, and they are stored secretly on a database that nobody has access to until the end of the game. We can then all review them, along with the world map at that turn, player stats etc.

It should be FUN!

Please do some jotting... Otherwise it will just be Joe, sneakily trying to write another epic memoir in 140 character bursts.

To get jotting, visit {} and choose a password. Have fun! Ask James if there are any problems with the site.

Love from James XXX""".format(civname, signed_link.decode()))
