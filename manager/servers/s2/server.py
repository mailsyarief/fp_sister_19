from backend import *
import Pyro4

servername = "server2"

def server():
    #JALANIN NAMESERVER LOCAL  pyro4-ns -n localhost -p 7777
    daemon = Pyro4.Daemon(host="10.151.253.253")
    ns = Pyro4.locateNS("10.151.253.253",7777)
    x_GreetServer = Pyro4.expose(Backend)
    uri_greetserver = daemon.register(x_GreetServer)
    print("URI greet server : ", uri_greetserver)
    ns.register(servername, uri_greetserver)
    daemon.requestLoop()

if __name__ == '__main__':
    server()

