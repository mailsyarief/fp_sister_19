import Pyro4

uri = "PYRONAME:server1@localhost:7777"

if __name__ == '__main__':
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






