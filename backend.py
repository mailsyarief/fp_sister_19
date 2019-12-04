import os
import json
import Pyro4

@Pyro4.behavior(instance_mode='single')
class Backend(object):
    # btn1 = 31998
    # btn2 = 31997
    # btn3 = 31996
    # btn4 = 31995
    # btn5 = 31994
    # btn6 = 31993
    # btn7 = 31992
    # btn8 = 31991
    # btn9 = 31990

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
        self.turn = 999
        self.lastTurn = 999
        pass

    def getTurn(self):
        return self.turn

    def resetTurn(self):
        self.lastTurn = self.turn
        self.turn = 999

    def setTurn(self,val):
        if(val != self.lastTurn):
            self.turn = val

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
        if(btnId == 1):
            self.btn1 = value
        elif(btnId == 2):
            self.btn2 = value
        elif(btnId == 3):
            self.btn3 = value
        elif(btnId == 4):
            self.btn4 = value
        elif(btnId == 5):
            self.btn5 = value
        elif(btnId == 6):
            self.btn6 = value
        elif(btnId == 7):
            self.btn7 = value
        elif(btnId == 8):
            self.btn8 = value
        elif(btnId == 9):
            self.btn9 = value

    def getBtn(self):
        statusBtn = [
            [1,self.btn1],
            [2,self.btn2],
            [3,self.btn3],
            [4,self.btn4],
            [5,self.btn5],
            [6,self.btn6],
            [7,self.btn7],
            [8,self.btn8],
            [9,self.btn9],
        ]
        
        return json.dumps(statusBtn, ensure_ascii=False)

    def checkIndex(self,userid):
        index = self.players.index(userid)
        self.setTurn(self.players[0])
        print "TURN : " + str(self.turn)
        if(index == 0):
            print str(index) + "->" + str(userid)
            return 'X'
        if(index == 1):
            print str(index) + "->" + str(userid)
            return 'O'

    def add_players(self,player_id):
        self.players.append(player_id)

    def get_players(self):
        return json.dumps(self.players, ensure_ascii=False)


if __name__ == '__main__':
    k = Backend()
