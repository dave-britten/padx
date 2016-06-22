#PADX Scraper

A simple screen-scaper for turning the list of guerilla dungeons on www.puzzledragonx.com into a calendar file (.ics) that can be subscribed to on your phone.

##Requirements

* Python 3
* BeautifulSoup4 Python module
* requests Python module
* A web server to host this script, and some familiarity with using cron (or similar facilities) to schedule it to run daily.

##Usage

Before initial usage, make sure you edit the script and change the values for 'group' and 'time_offset'.

When that's done, simply execute padx.py to generate pad-a.ics (or pad-b.ics, pad-c.ics, etc. depending on group) in the current working directory. You may optionally specify an output file path as a single command line argument, e.g.:

    padx.py /var/www/html/pad-b.ics

##License

Copyright (c) 2016 Dave Britten

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.