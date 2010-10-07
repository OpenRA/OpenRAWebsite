#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import logging
from server import *
        
class MotdHandler(webapp.RequestHandler):
    def get(self):
        if not self.request.get('v'): return
        try:
            version = int(self.request.get('v').partition('-')[2])
            if version < Server.LATEST_VERSION:
                self.response.out.write(Server.NEW_VERSION_AVAILABLE)
            else:
                self.response.out.write(Server.MOTD)
        except Exception, ex:
            logging.error(ex)
            self.response.out.write(Server.MOTD)
        
        
class ListHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"
        n = 0
        for gameinfo in Server.GetGames():
            self.response.out.write('Game@%d:\n' % n)
            for key in gameinfo.keys():
                self.response.out.write('\t%s: %s\n' % (key, gameinfo[key]))
            n += 1
            
    
class PingHandler(webapp.RequestHandler):
    def get(self):
        if not self.request.get('port'): return
        if not self.request.get('name'): return
        if not self.request.get('state'): return
        if not self.request.get('map'): return
        if not self.request.get('mods'): return
        if not self.request.get('players'): return
        
        try:
            ip = self.request.remote_addr
            if self.request.get('new'):
                if not self.CheckPort(ip, self.request.get('port')):
                    return
                key = Server.NewGame(
                               self.request.get('name'), 
                               self.request.remote_addr, 
                               self.request.get('port'), 
                               self.request.get('players'), 
                               self.request.get('state'), 
                               self.request.get('map'), 
                               self.request.get('mods'))
            else:
                key = Server.UpdateGame(
                               self.request.get('name'), 
                               self.request.remote_addr, 
                               self.request.get('port'), 
                               self.request.get('players'), 
                               self.request.get('state'), 
                               self.request.get('map'), 
                               self.request.get('mods'))
        except Exception, ex:
            logging.error(ex)
        
    def CheckPort(self, ip, port):
        return True
        

def main():
    application = webapp.WSGIApplication([('/list', ListHandler),
                                          ('/motd', MotdHandler),
                                          ('/ping', PingHandler)
                                          ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
