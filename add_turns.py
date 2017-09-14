from datetime import datetime
import os
from glob import glob
from new_turn import get_year, get_turn
from application.models import Turn

files = glob('/home/freeciv/freeciv-current/saves/*.bz2')
for f in files:
	filename=os.path.basename(f)
	timestamp=datetime.fromtimestamp(os.path.getmtime(f))
	print(timestamp,get_year(filename),get_turn(filename))
	Turn.create(timestamp=timestamp, number=get_turn(filename), year=get_year(filename))
