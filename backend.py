import os
import json
import Pyro4

@Pyro4.behavior(instance_mode='single')
class Backend(object):

    def __init__(self):
        self.btn1 = ''
        self.btn2 = ''
        self.btn3 = ''
        self.btn4 = ''
        self.btn5 = ''
        self.btn6 = ''
        self.btn7 = ''
        self.btn8 = ''
        self.btn9 = ''
        # self.spectator = []
        self.players = []
        pass

    def show(self):
        return "ok"

    def resetFlag(self):
        self.btn1 = ''
        self.btn2 = ''
        self.btn3 = ''
        self.btn4 = ''
        self.btn5 = ''
        self.btn6 = ''
        self.btn7 = ''
        self.btn8 = ''
        self.btn9 = ''

    def setBtn(self,id,value):
        print str(id)+" "+str(value)
        btnId = id
        if(btnId == -2008):
            self.btn1 = value
        elif(btnId == -2009):
            self.btn2 = value
        elif(btnId == -2010):
            self.btn3 = value
        elif(btnId == -2011):
            self.btn4 = value
        elif(btnId == -2012):
            self.btn5 = value
        elif(btnId == -2013):
            self.btn6 = value
        elif(btnId == -2014):                                                            
            self.btn7 = value
        elif(btnId == -2015):            
            self.btn8 = value
        elif(btnId == -2016):            
            self.btn9 = value

    def getBtn(self):
        statusBtn = [
            [-2008,self.btn1],
            [-2009,self.btn2],
            [-2010,self.btn3],
            [-2011,self.btn4],
            [-2012,self.btn5],
            [-2013,self.btn6],
            [-2014,self.btn7],
            [-2015,self.btn8],
            [-2016,self.btn9],
        ]
        
        return json.dumps(statusBtn, ensure_ascii=False)

        
    def add_players(self,player_id):
        self.players.append(player_id)

    def get_players(self):
        return json.dumps(self.players, ensure_ascii=False)


if __name__ == '__main__':
    k = Backend()
