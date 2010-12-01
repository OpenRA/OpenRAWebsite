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
import logging, urllib
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
from google.appengine.api.labs import taskqueue
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
        i = 0
        for gameinfo in Server.GetGames():
            self.response.out.write('Game@%d:\n' % i)
            for key in gameinfo.keys():
                self.response.out.write('\t%s: %s\n' % (key, gameinfo[key]))
            i += 1
            
    
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
                Server.NewGame(
                               self.request.get('name'), 
                               ip, 
                               self.request.get('port'), 
                               self.request.get('players'), 
                               self.request.get('state'), 
                               self.request.get('map'), 
                               self.request.get('mods'))
                # check port
                taskqueue.add(url='/task/checkPort', params={'ip': ip, 'port': self.request.get('port')})
            #elif self.request.get('die'):
            else:
                Server.UpdateGame(
                               self.request.get('name'), 
                               ip, 
                               self.request.get('port'), 
                               self.request.get('players'), 
                               self.request.get('state'), 
                               self.request.get('map'), 
                               self.request.get('mods'))
        except Exception, exception:
            logging.exception(exception)


class TaskCheckPort(webapp.RequestHandler):
    REMOTE_PING_SERVICE_URL = "http://localhost/service/ping.php" #TODO: set me
    def post(self):
        try:
            requestData = urllib.urlencode({
                    'ip': self.request.get('ip'),
                    'port': self.request.get('port'),
                    })
            result = urlfetch.fetch(url=self.REMOTE_PING_SERVICE_URL,
                        payload=requestData,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'})
            if result.status_code == 200:
                if result.content is not True: #TODO: set value for a valid response
                    Server.EndGame(self.request.get('ip'), self.request.get('port'))
        except Exception, exception:
            logging.exception(exception)

def main():
    application = webapp.WSGIApplication([('/list', ListHandler),
                                          ('/motd', MotdHandler),
                                          ('/ping', PingHandler),
                                          ('/task/checkPort', TaskCheckPort),
                                          ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
