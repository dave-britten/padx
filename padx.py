#! /usr/bin/python3

import sys
import requests
import re
import uuid
from datetime import datetime, date, time, timedelta
from bs4 import BeautifulSoup

#Set your group here.
group = 'c'
#Time offset in hours. PADX reports times in Pacific by default (and that's the easiest way
#to ensure that the 3:00 AM day cutoff is interpreted properly). Set to the numbe of
#hours to add/subtract to get to your timezone. (e.g. 3 = Eastern time)
time_offset = 3

#Default output file if not given on the command line.
outfile = "padx-" + group + ".ics"
if len(sys.argv) > 1:
    outfile = sys.argv[1]

group = group.lower() #Normalize, just in case.
#Fetch the front page
r = requests.get("http://www.puzzledragonx.com")
t = r.text
soup = BeautifulSoup(t, 'html.parser')
#Grab the metal/guerilla schedule div.
metal = soup.find("div", id="metal1a").find("table", id="event")

#Turn the group letter into a numeric value for indexing into the correct table cells.
groupoffset = ['a', 'b', 'c', 'd', 'e'].index(group.lower())

ics = open(outfile, 'w')
ics.write("BEGIN:VCALENDAR\n")
ics.write("PRODID:-//Dave Britten//PAD//EN\n")
ics.write("VERSION:2.0\n")
ics.write("METHOD:PUBLISH\n")
ics.write("X-WR-CALNAME:Puzzle & Dragons Group " + group.upper() + "\n")

#Dungeons are given in row pairs, with the first row containing the icon/link,
#and the second showing the time.
for i in range(1, len(metal.contents), 2):
    #Drill down to the dungeon icon.
    tr_icon = metal.contents[i]
    td_icon = tr_icon.contents[groupoffset * 3]
    a_icon = tr_icon.a

    #No icon in the cell. Fewer dungeons than normal today, maybe?
    if a_icon == None:
        continue

    #Get the time cell, and extract the text.    
    tr_time = metal.contents[i + 1]
    td_time = tr_time.contents[groupoffset * 2]
    timestr = td_time.text

    #Request the page that the icon links to, to get the dungeon name.
    r = requests.get("http://www.puzzledragonx.com/" + a_icon["href"])
    soup = BeautifulSoup(r.text, 'html.parser')
    loc_div = soup.find("div", id="location")
    dname = loc_div.contents[4].text

    #Parse the dungeon time. (Hours, optional :minutes, and am/pm)
    time_re = re.search('(?P<hr>\d+)(?:\:(?P<mn>\d+))?\s(?P<t>[a|p]m)', timestr, re.IGNORECASE)

    hr = int(time_re.group('hr'))
    mn = int(time_re.group('mn')) if time_re.group('mn') else 0
    t = time_re.group('t')
    #Convert to 24-hour
    tm = time((hr % 12) + (0 if t == "am" else 12), mn)

    dt = datetime.combine(date.today(), tm)
    #Dungeons between midnight and 04:00 are actually for tomorrow morning; add one day.
    if tm < time(4):
        dt = dt + timedelta(days=1)
    #Timezone conversion.
    if time_offset:
        dt = dt + timedelta(hours=time_offset)

    #print("{0}, {1}".format(dname, dt))

    ics.write("BEGIN:VEVENT\n")
    ics.write("DTSTART:" + dt.strftime("%Y%m%dT%H%M%S") + "\n")
    ics.write("DTEND:" + (dt + timedelta(hours=1)).strftime("%Y%m%dT%H%M%S") + "\n")
    ics.write("UID:" + str(uuid.uuid4()) + "\n")
    ics.write("CLASS:PUBLIC\n")
    ics.write("CREATED:" + datetime.now().strftime("%Y%m%dT%H%M%S") + "\n")
    ics.write("SUMMARY:" + dname + "\n")
    ics.write("BEGIN:VALARM\n")
    ics.write("TRIGGER:-PT0M\n") #Alarm at the event time (0-minute lead)
    ics.write("ACTION:DISPLAY\n")
    ics.write("END:VALARM\n")
    ics.write("END:VEVENT\n")

ics.write("END:VCALENDAR\n")
ics.close()


# License
# Copyright (c) 2016 Dave Britten
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
