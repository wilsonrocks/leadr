import sys
import re
from datetime import datetime

from application.models import Turn

regex = r'epoch4-T(\d{4})-Y([-\d]\d{4})'

def get_turn(filename):
    m = re.match(regex, filename)
    return int(m.group(1))

def get_year(filename):
    m = re.match(regex, filename)
    year = m.group(2)
    if year[0] == '-':
            return str(int(year[1:]))+'BC'
    else:
            return str(int(year))+'AD'

if __name__ == "__main__":
	filename = sys.argv[1]
	print(get_turn(filename))
	print(get_year(filename))
	print(datetime.now())

	Turn.create(number=get_turn(filename), year= get_year(filename)) #timestamp is set to NOW by default but this script is running via cron
