#! /usr/bin/python3

import requests
import re
import uuid
from datetime import datetime, date, time, timedelta
from bs4 import BeautifulSoup

group = 'c'
time_offset = 3

r = requests.get("http://www.puzzledragonx.com")
t = r.text
soup = BeautifulSoup(t, 'html.parser')
metal = soup.find("div", id="metal1a").find("table", id="event")

groupoffset = ['a', 'b', 'c', 'd', 'e'].index(group.lower())
print("Group offset: " + str(groupoffset))

ics = open('/var/www/html/dave.brittens.org/pad-c.ics', 'w')
ics.write("BEGIN:VCALENDAR\n")
ics.write("PRODID:-//Dave Britten//PAD//EN\n")
ics.write("VERSION:2.0\n")
ics.write("METHOD:PUBLISH\n")
ics.write("X-WR-CALNAME:Puzzle & Dragons Group C\n")

for i in range(1, len(metal.contents), 2):
    tr_icon = metal.contents[i]
    td_icon = tr_icon.contents[groupoffset * 3]
    a_icon = tr_icon.a

    if a_icon == None:
        continue
    
    tr_time = metal.contents[i + 1]
    td_time = tr_time.contents[groupoffset * 2]
    timestr = td_time.text

    r = requests.get("http://www.puzzledragonx.com/" + a_icon["href"])
    soup = BeautifulSoup(r.text, 'html.parser')
    loc_div = soup.find("div", id="location")
    dname = loc_div.contents[4].text


    time_re = re.search('(?P<hr>\d+)(?:\:(?P<mn>\d+))?\s(?P<t>[a|p]m)', timestr, re.IGNORECASE)

    hr = int(time_re.group('hr'))
    mn = int(time_re.group('mn')) if time_re.group('mn') else 0
    t = time_re.group('t')

    dt = datetime.combine(date.today(), time(hr + (12 if t == 'pm' else 0), mn))
    if time_offset:
        dt = dt + timedelta(hours=time_offset)

    print("{0}, {1}".format(dname, dt))

    ics.write("BEGIN:VEVENT\n")
    ics.write("DTSTART:" + dt.strftime("%Y%m%dT%H%M%S") + "\n")
    ics.write("DTEND:" + (dt + timedelta(hours=1)).strftime("%Y%m%dT%H%M%S") + "\n")
    ics.write("UID:" + str(uuid.uuid4()) + "\n")
    ics.write("CLASS:PUBLIC\n")
    ics.write("CREATED:" + datetime.now().strftime("%Y%m%dT%H%M%S") + "\n")
    ics.write("SUMMARY:" + dname + "\n")
    ics.write("BEGIN:VALARM\n")
    ics.write("TRIGGER:-PT5M\n")
    ics.write("ACTION:DISPLAY\n")
    ics.write("END:VALARM\n")
    ics.write("END:VEVENT\n")

ics.write("END:VCALENDAR\n")
ics.close()
