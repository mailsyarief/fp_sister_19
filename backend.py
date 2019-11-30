import os

class Backend(object):

    def __init__(self):
        self.btn1 = False
        self.btn2 = False
        self.btn3 = False
        self.btn4 = False
        self.btn5 = False
        self.btn6 = False
        self.btn7 = False
        self.btn8 = False
        self.btn9 = False
        pass

    def show(self):
        return "ok"
    
    def setBtn(self,id):
        return "PYRO : "+id

    def getBtn(self):
        return -2009


if __name__ == '__main__':
    k = Backend()
