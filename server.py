"""
Module for the CAL Leadership Insitute September 2013 Presentation

Copyright (C) 2013 Jeremy Nelson 

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
__author__ = "Jeremy Nelson"

import argparse
import datetime
import json
import os

from bottle import abort, request, route, run, static_file
from bottle import jinja2_view as view
from bottle import jinja2_template as template

from collections import OrderedDict

FLUP = False
PROJECT_ROOT = os.path.split(os.path.abspath(__name__))[0]
SLIDES = OrderedDict()
for slide in json.load(
    open(os.path.join(
        PROJECT_ROOT,
        "assets",
        "js",
        "slides.json"))):
    SLIDES[slide.get('name')] = slide
SOURCES = {}
for filename in ["a-very-brief-introduction-to-open-access",
                 "futures-thinking-basics",
                 "power-of-pull"]:
    SOURCES[filename] = json.load(
        open(os.path.join(PROJECT_ROOT,
                          "assets",
                          "js",
                          "{0}.json".format(filename))))

@route('/calli-2013-presentation/assets/<type_of:path>/<filename:path>')
def send_asset(type_of,filename):
    local_path = os.path.join(PROJECT_ROOT,
                              "assets",
                              type_of,
                              filename)
    if os.path.exists(local_path):
        return static_file(filename,
			   root=os.path.join(PROJECT_ROOT,
                                             "assets",
                                             type_of))
    

@route("/calli-2013-presentation/glossary.html")
def glossary():
    return template("glossary.html",
                    category='resources',
                    current=None,
                    slides=SLIDES)

@route("/calli-2013-presentation/slides/<slide:path>")
def slide(slide):
    
    return template("{0}.html".format(slide),
                    category='slide',
                    current=SLIDES.get(slide),
                    slides=SLIDES)

@route("/calli-2013-presentation/sources.html")
def sources():
    sorted_sources = []
    for key in sorted(SOURCES.keys()):
        sorted_sources.append(SOURCES[key])
    return template("sources.html",
                    category='resources',
                    current=None,
                    sources=sorted_sources,
                    slides=SLIDES)
    
@route("/calli-2013-presentation/")
def index():
    return template("index.html",
                    current=None,
                    slides=SLIDES)


parser = argparse.ArgumentParser(
    description='Run CALLI 2013 Presentation')
parser.add_argument('mode',
                    help='Run in either prod (production) or dev (development)')

mode = parser.parse_args().mode
if mode == 'prod': 
    run(server=FlupFCGIServer,
        host='0.0.0.0',
        port=9024)
elif mode == 'dev':
    run(host='0.0.0.0', 
        port=9024,
        debug=True,
        reloader=True)
else:
    print("ERROR unknown run mode {0}".format(mode))
