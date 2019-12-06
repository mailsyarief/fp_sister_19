import Pyro4
import json

class Backend():
    def __init__(self):
        self.readLocalJson()
        self.json = ''
        self.server = ''
        self.managers = ["manager1"]
        print self.json
        pass

    def broadcast(self):
        for x in self.managers:
            uri = "PYRONAME:{}@10.151.30.141:7778" .format(x)
            self.server = Pyro4.Proxy(uri)
            self.readLocalJson()
            self.server.setServerJSON(self.json)
            self.server.writeLocalJson()
            self.server.askServerToSync()
            self.server.cobaPrint()
            print "broadcast done"

    def cobaPrint(self):
        print "WKWKWKWKWKWKKW"

    def readLocalJson(self):
        with open('log.json') as f:
            data = json.load(f)
            self.json = data

    def askServerToSync(self):
        servername = "server2"
        uri = "PYRONAME:{}@localhost:7777".format(servername)
        self.server = Pyro4.Proxy(uri)
        self.setServerJSON(unicode(self.json,'utf-8'))
        self.server.readLocalJson()
        print "ask to sync done"

    def writeLocalJson(self):
        with open('log.json', 'w') as json_file:
            json.dump(self.json, json_file)

    def setServerJSON(self, json):
        self.json = json
        self.writeLocalJson()

servername = "manager2"
def server():
    #JALANIN NAMESERVER LOCAL  pyro4-ns -n localhost -p 7777
    daemon = Pyro4.Daemon(host="10.151.30.143")
    ns = Pyro4.locateNS("10.151.30.143",7778)
    x_GreetServer = Pyro4.expose(Backend)
    uri_greetserver = daemon.register(x_GreetServer)
    print("URI greet server : ", uri_greetserver)
    ns.register(servername, uri_greetserver)
    daemon.requestLoop()

if __name__ == '__main__':
    server()

