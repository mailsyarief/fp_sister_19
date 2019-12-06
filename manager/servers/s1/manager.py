import Pyro4
import json

class Backend():
    def __init__(self):
        self.json = ''
        self.server = ''
        self.managers = ["manager2"]
        pass

    def broadcast(self):
        for x in self.managers:
            uri = "PYRONAME:{}@localhost:7777" .format(x)
            self.server = Pyro4.Proxy(uri)
            self.setServerJSON(self.json)
            self.writeLocalJson()
            self.askServerToSync()
            print "broadcast done"

    def askServerToSync(self):
        servername = "server1"
        uri = "PYRONAME:{}@localhost:7777".format(servername)
        self.server = Pyro4.Proxy(uri)
        self.setServerJSON(self.json)
        self.server.readLocalJson()
        print "ask to sync done"

    def writeLocalJson(self):
        with open('log.json', 'w') as json_file:
            json.dump(self.json, json_file)

    def setServerJSON(self, json):
        self.json = json
        self.writeLocalJson()

servername = "manager1"
def server():
    #JALANIN NAMESERVER LOCAL  pyro4-ns -n localhost -p 7777
    daemon = Pyro4.Daemon(host="localhost")
    ns = Pyro4.locateNS("localhost",7777)
    x_GreetServer = Pyro4.expose(Backend)
    uri_greetserver = daemon.register(x_GreetServer)
    print("URI greet server : ", uri_greetserver)
    ns.register(servername, uri_greetserver)
    daemon.requestLoop()

if __name__ == '__main__':
    server()

