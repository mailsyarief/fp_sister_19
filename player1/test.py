import Pyro4


uri = "PYRONAME:maile@localhost:7777"

if __name__=='__main__':
    server = Pyro4.Proxy(uri)



    print server.get_players()
    