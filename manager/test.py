import Pyro4



if __name__ == '__main__':
    nameserver = ['manager2']
    for x in nameserver:
        uri = "PYRONAME:{}@10.151.30.134:7778".format(x)
        server = Pyro4.Proxy(uri)
        # server.resetLocalJson()
        print server.cobaPrint()
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






