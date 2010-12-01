
import os
import logging
import datetime
from google.appengine.ext import db
from google.appengine.ext.db import Key

class Server:
    NEW_VERSION_AVAILABLE = 'New version available. Please go to http://open-ra.org to upgrade.'
    MOTD = 'Welcome to OpenRA. Read news and more at http://reddit.com/r/openra.'
    LATEST_VERSION = 1
    STALE_DURATION = datetime.timedelta(seconds=300)
    
    def NewGame(self, name, ip, port, players, state, map, mods):
        try:
            game = Game(name=name, ip=ip, port=int(port), players=int(players), 
                            state=int(state), map=map, mods=mods)
            game.put()
        except Exception, exception:
            logging.exception(exception)
    NewGame = classmethod(NewGame)
    
    def UpdateGame(self, name, ip, port, players, state, map, mods):
        try:
            games = []
            game = db.GqlQuery("SELECT * FROM Game where ip = :1 AND port = :2 AND lastPingTime >= :3 ORDER BY lastPingTime DESC", 
                                        ip, int(port), now - Server.STALE_DURATION).get()
            if game:
                game.name = name
                game.ip = ip
                game.port = int(port)
                game.players = int(players)
                game.state = int(state)
                game.map = map
                game.mods = mods
                game.put()
        except Exception, exception:
            logging.exception(exception)
    UpdateGame = classmethod(UpdateGame)
    
    def EndGame(self, ip, port):
        try:
            #end ALL games on this ip / port
            games = db.GqlQuery("SELECT * FROM Game where ip = :1 AND port = :2", ip, int(port))
            for game in games:
                game.delete()
        except Exception, exception:
            logging.exception(exception)
    EndGame = classmethod(EndGame)
    
    def GetGames(self):
        try:
            now = datetime.datetime.now()
            games = []
            currentGames = db.GqlQuery("SELECT * FROM Game where lastPingTime >= :1 ORDER BY lastPingTime DESC", now - Server.STALE_DURATION)
            for game in currentGames:
                ttl = Server.STALE_DURATION.seconds - (now - game.lastPingTime).seconds
                games.append({
                          'Name': game.name,
                          'Address': "%s:%d" % (game.ip, game.port),
                          'State': str(game.state),
                          'Players': str(game.players),
                          'Map': game.map,
                          'Mods': game.mods,
                          'TTL': str(ttl),
                          })
            return games
        except Exception, exception:
            logging.exception(exception)
    GetGames = classmethod(GetGames)
    
class Game(db.Model):
    name = db.StringProperty()
    ip = db.StringProperty()
    port = db.IntegerProperty()
    players = db.IntegerProperty()
    state = db.IntegerProperty()
    lastPingTime = db.DateTimeProperty(auto_now=True)
    map = db.StringProperty()
    mods = db.StringProperty()
