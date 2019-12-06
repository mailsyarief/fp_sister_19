import Pyro4



if __name__ == '__main__':
    nameserver = ['server2','server3','server1']
    for x in nameserver:
        uri = "PYRONAME:{}@localhost:7777".format(x)
        server = Pyro4.Proxy(uri)
        server.resetLocalJson()
        print server.getServerJson()
    # server.add_player("P1")
    # server.add_player("P2")
    # server.add_player("P3")
    # server.add_player("P4")
    # print server.getServerJson()
    # server.writeLocalJson()
    # server.readLocalJson()
    # print server.getServerJson()
    # server.resetLocalJson()
    # server.readLocalJson()
    # print server.getServerJson()






