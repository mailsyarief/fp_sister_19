import os
import json
import Pyro4

@Pyro4.behavior(instance_mode='single')
class Backend(object):
    def __init__(self):
        self.json = ''
        self.resetLocalJson()
        self.readLocalJson()
        self.mymanageraddress = "10.151.30.143"
        pass

    def doBroadcast(self):
        uri = "PYRONAME:manager1@{}:7778".format(self.mymanageraddress)
        manager = Pyro4.Proxy(uri)
        manager.setServerJSON(self.json)
        manager.broadcast()


    def replacePlayer(self,username):
        if(len(self.json['spectators'])  >= 0 ):
            if username in self.json['players']:
                index = self.json['players'].index(username)
                self.json['players'][index] = self.json['spectators'][0]
                self.json['spectators'].pop(0)
                if(self.json['turn'] == username):
                    self.json['turn'] = self.json['players'][index]
            elif username in self.jsonp['spectators']:
                self.json['spectators'].remove(username)
        else:
            self.json['players'].remove(username)

        print self.json['players']
        print self.json['spectators']
        print self.json['turn']

        self.syncJson()


    def syncJson(self):
        self.writeLocalJson()
        self.readLocalJson()
        self.doBroadcast()

    def readLocalJson(self):
        with open('log.json') as f:
            data = json.load(f)
            self.json = data

    def getServerJson(self):
        return self.json

    def writeLocalJson(self):
        with open('log.json', 'w') as json_file:
            json.dump(self.json, json_file)

    def addPlayer(self, username):
        self.readLocalJson()
        if(len(self.json['players']) < 2):
            if username not in self.json['players']:
                self.json['players'].append(username)
        else:
            self.addSpectator(username)
        self.syncJson()

    def addSpectator(self, username):
        if username not in self.json['spectators']:
            self.json['spectators'].append(username)
            self.syncJson()

    def resetLocalJson(self):
        with open('plain.log.json') as f:
            data = json.load(f)
            self.json = data
            self.writeLocalJson()

    #---------------------------------

    def checkXO(self, username):
        try:
            index = self.json['players'].index(username)
            self.setTurn(self.json['players'][0])
            self.syncJson()
            if (index == 0):
                return 'X'
            if (index == 1):
                return 'O'
        except:
            return '-'

    def setTurn(self,username):
        print self.json['lastTurn']
        if(username != self.json['lastTurn']):
            self.json['turn'] = username
            self.syncJson()

    def getTurn(self):
        return self.turn

    def resetTurn(self):
        print "RESET"
        if(self.json['turn'] == self.json['players'][1]):
            self.json['turn'] = self.json['players'][0]
        elif(self.json['turn'] == self.json['players'][0]):
            self.json['turn'] = self.json['players'][1]
        self.syncJson()

    def setBtn(self,btnId,value):
        self.json['flag'][btnId] = value
        self.syncJson()

    def getBtn(self):
        return self.json['flag']



if __name__ == '__main__':
    k = Backend()
