import cherrypy
import os
from goniometer import Goniometer
from history import History

root = Goniometer()
root.history = History()

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.config.update({'server.socket_host': '192.168.1.148'})
    cherrypy.quickstart(root, '/', conf)
