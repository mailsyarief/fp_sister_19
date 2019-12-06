import json
import time
import wx
import Pyro4
import wx.lib.buttons as buttons
from threading import Thread

EVT_RESULT_ID = wx.NewId()


def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)


class ResultEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data


########################################################################

class TestThread(Thread):
    def __init__(self, wxObject):
        Thread.__init__(self)
        self.wxObject = wxObject
        uri = "PYRONAME:server3@localhost:7777"
        self.server = Pyro4.Proxy(uri)
        self.alive = True
        self.start()

    def run(self):
        while self.alive:
            jsonData = self.server.getServerJson()
            print jsonData
            time.sleep(0.5)
            wx.PostEvent(self.wxObject, ResultEvent(jsonData))


########################################################################

class MyForm(wx.Frame):
    def __init__(self):
        size = (400, 500)
        wx.Frame.__init__(self, None, wx.ID_ANY, "Player 3", size=size)
        self.Toggled = False
        self.playerWon = False
        self.player = ''
        self.font = ''
        self.server = ''
        self.title = ''
        self.username = 'P3'
        self.pyro_client()
        self.isFinish = False
        self.isSpectator = False
        self.tretTret = TestThread(self)

        textSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.fgSizer = wx.FlexGridSizer(rows=3, cols=3, vgap=5, hgap=5)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD)

        size = (100, 100)
        self.button1 = buttons.GenToggleButton(self, id=0, size=size, name="btn1")
        self.button2 = buttons.GenToggleButton(self, id=1, size=size, name="btn2")
        self.button3 = buttons.GenToggleButton(self, id=2, size=size, name="btn3")
        self.button4 = buttons.GenToggleButton(self, id=3, size=size, name="btn4")
        self.button5 = buttons.GenToggleButton(self, id=4, size=size, name="btn5")
        self.button6 = buttons.GenToggleButton(self, id=5, size=size, name="btn6")
        self.button7 = buttons.GenToggleButton(self, id=6, size=size, name="btn7")
        self.button8 = buttons.GenToggleButton(self, id=7, size=size, name="btn8")
        self.button9 = buttons.GenToggleButton(self, id=8, size=size, name="btn9")
        self.normalBtnColour = self.button1.GetBackgroundColour()

        self.widgets = [self.button1, self.button2, self.button3,
                        self.button4, self.button5, self.button6,
                        self.button7, self.button8, self.button9]

        for button in self.widgets:
            button.SetFont(font)
            button.Bind(wx.EVT_BUTTON, self.onToggle)

        self.fgSizer.AddMany(self.widgets)
        mainSizer.Add(self.fgSizer, 0, wx.ALL | wx.CENTER, 5)

        self.titleText = wx.StaticText(self, label='')
        textSizer.Add(self.titleText, 0, wx.CENTER)

        self.endTurnBtn = wx.Button(self, label="DEBUG")
        # self.endTurnBtn.Bind(wx.EVT_BUTTON, self.printFlag)
        btnSizer.Add(self.endTurnBtn, 0, wx.ALL | wx.CENTER, 5)

        startOverBtn = wx.Button(self, label="Restart")
        # startOverBtn.Bind(wx.EVT_BUTTON, self.onRestart)
        btnSizer.Add(startOverBtn, 0, wx.ALL | wx.CENTER, 5)
        mainSizer.Add(textSizer, 0, wx.CENTER)
        mainSizer.Add(btnSizer, 0, wx.CENTER)

        self.setInitial()

        self.methodsToWin = [(self.button1, self.button2, self.button3),
                             (self.button4, self.button5, self.button6),
                             (self.button7, self.button8, self.button9),
                             (self.button1, self.button4, self.button7),
                             (self.button2, self.button5, self.button8),
                             (self.button3, self.button6, self.button9),
                             (self.button1, self.button5, self.button9),
                             (self.button3, self.button5, self.button7)]

        self.SetSizer(mainSizer)

        EVT_RESULT(self, self.getThreadData)

    def onToggle(self, event):
        self.checkWin()
        if not self.Toggled:
            button = event.GetEventObject()
            button.SetLabel(self.player)
            button_id = button.GetId()

            self.server.setBtn(button_id, self.player)

            self.Toggled = True
            print "if not"
            self.endTurnBtn.Enable()
            for btn in self.widgets:
                if button_id != btn.GetId():
                    btn.Disable()
            self.titleText.SetLabel("...")
            self.server.resetTurn()
        else:
            print "else"

        if not self.playerWon:
            labels = [True if btn.GetLabel() else False for btn in self.widgets]
            if False not in labels:
                msg = "Draw..."
                dlg = wx.MessageDialog(None, msg, "Game Over!",
                                       wx.YES_NO | wx.ICON_WARNING)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                    self.restart()
                dlg.Destroy()

    def pyro_client(self):
        uri = "PYRONAME:server3@localhost:7777"
        self.server = Pyro4.Proxy(uri)
        self.server.addPlayer(self.username)

    def setInitial(self):
        TestThread(self)
        self.player = self.server.checkXO(self.username)
        print "MY INITIAL IS " + self.player
        if(self.player == 'X'):
            self.Toggled = False
        elif(self.player == 'O'):
            self.titleText.SetLabel("WAIT FOR OTHER PLAYER")
            self.Toggled = True
            for btn in self.widgets:
                btn.Disable()
        else:
            self.titleText.SetLabel("WELCOME SPECTATOR!")
            self.isSpectator = True
            self.Toggled = True
            for btn in self.widgets:
                btn.Disable()


    def enableUnusedButtons(self):
        for button in self.widgets:
            if button.GetLabel() == "":
                button.Enable()
        self.Refresh()
        self.Layout()

    def checkWin(self, computer=False):
        if (self.isFinish == False):
            for button1, button2, button3 in self.methodsToWin:
                if button1.GetLabel() == button2.GetLabel() and \
                        button2.GetLabel() == button3.GetLabel() and \
                        button1.GetLabel() != "":

                    self.playerWon = True
                    self.isFinish = True
                    button1.SetBackgroundColour("Yellow")
                    button2.SetBackgroundColour("Yellow")
                    button3.SetBackgroundColour("Yellow")
                    self.Layout()

                    if not computer:
                        msg = "Selamat Player " + button1.GetLabel() + " menang! main lagi?"
                        dlg = wx.MessageDialog(None, msg, "Winner!",
                                               wx.YES_NO | wx.ICON_WARNING)
                        result = dlg.ShowModal()
                        if result == wx.ID_YES:
                            wx.CallAfter(self.restart)
                        dlg.Destroy()
                        break
                    else:
                        return True

    def updateView(self):
        data = self.server.getBtn()
        for index, value in enumerate(data, start=0):
            for button in self.widgets:
                if (index == button.GetId()):
                    if (value != ''):
                        button.SetLabel(value)
                    button.SetValue(True)

        self.checkWin()
        self.Refresh()
        self.Layout()

    def getThreadData(self, msg):
        data = msg.data
        print data['turn']
        self.checkYourTurn(data['turn'])

    def checkYourTurn(self, data):
        if(self.isSpectator == False):
            if (self.username == data):
                print "THIS IS YOUR TURN"
                self.titleText.SetLabel("THIS IS YOUR TURN")
                self.Toggled = False
                self.enableUnusedButtons()
            else:
                self.titleText.SetLabel("WAIT FOR OTHER PLAYER")
                self.updateView()
                self.disableAllBtn()
        else:
            self.titleText.SetLabel("WELCOME SPECTATOR!")
            self.updateView()
            self.disableAllBtn()

    def disableAllBtn(self):
        for button in self.widgets:
            button.Disable()
        self.Refresh()
        self.Layout()


if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()
