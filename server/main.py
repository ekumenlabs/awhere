#!/usr/bin/python
import cherrypy
import redis

'''
Glossary:
 akeys                  Awareness keys

Keyspace:
 :akeys:<username>      set | defined akeys for this user
 <username>:<akey>      string | value for this akey and user
'''

class Store:
    def __init__(self):
        self._r = redis.Redis("localhost")

    @cherrypy.expose
    def test(self):
        return "working."

    @cherrypy.expose
    def report(self, userid, akey, avalue):
        self._r.sadd(":akeys:%s" % userid, akey)
        self._r.set("%s:%s" % (userid,akey), avalue)
        return "stored"

    @cherrypy.expose
    def query(self, userid, akey=None):
        if type(akey) != list:
            akey = [ akey ]
        if akey[0] is None:
            akey = self._r.smembers(":akeys:%s" % userid)
        pairs = map(lambda x: "'%s':'%s'" % (x, self._r.get("%s:%s" % (userid,x))), akey)
        result = "{" + ",".join(pairs) + "}"
        return result

cherrypy.quickstart(Store())
