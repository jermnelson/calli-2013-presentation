"""
Module for the CAL Leadership Insitute September 2013 Presentation
"""
__author__ = "Jeremy Nelson"

import datetime
import json
import os

from bottle import abort, request, route, run, static_file
from bottle import template

FLUP = False
PROJECT_ROOT = os.path.split(os.path.abspath(__name__))[0]

@route('/assets/<type_of:path>/<filename:path>')
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
    


@route("/")
@route("/calli-2013-presentation/")
def index():
    return template("index")

if FLUP is True:
    run(server=FlupFCGIServer,
        host='0.0.0.0',
        port=9024)
else:
    run(host='0.0.0.0', 
        port=9024,
        debug=True,
        reloader=True)
