#!/home2/mudayne1/python/bin/python
import sys, os
sys.path.insert(0,"/home2/mudayne1/python")

from flup.server.fcgi import WSGIServer
from blog import app as application

WSGIServer(application).run()
