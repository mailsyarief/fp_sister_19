import json
import time
import wx
import Pyro4
import wx.lib.buttons as buttons
from threading import Thread

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()


def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)


class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data


########################################################################
class TestThread(Thread):
    """Test Worker Thread Class."""

    # ----------------------------------------------------------------------
    def __init__(self, wxObject):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.wxObject = wxObject
        uri = "PYRONAME:maile@localhost:7777"
        self.server = Pyro4.Proxy(uri)
        self.alive = True

        # self.start()  # start the thread


    # ----------------------------------------------------------------------
    def go(self):
        self.join()

    def abort(self):
        self.alive = False

    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        # for i in range(6):
        #     time.sleep(10)
        #     amtOfTime = (i + 1) * 10
        #     wx.PostEvent(self.wxObject, ResultEvent(amtOfTime))
        # time.sleep(5)
        a = 0
        while self.alive:
            a = self.server.getTurn()
            time.sleep(1)
            print a
            wx.PostEvent(self.wxObject, ResultEvent(a))


        wx.PostEvent(self.wxObject, ResultEvent("Thread finished!"))


########################################################################
class MyForm(wx.Frame):

    # ----------------------------------------------------------------------
    def __init__(self):
        size = (400, 500)
        wx.Frame.__init__(self, None, wx.ID_ANY, "Player 1", size=size)
        self.Toggled = False
        self.playerWon = False
        self.player = ''
        self.font = ''
        self.server = ''
        self.title = ''
        self.playerId = 2
        self.pyro_client()
        self.tretTret = TestThread(self)


        # Add a panel so it looks the correct on all platforms

        textSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.fgSizer = wx.FlexGridSizer(rows=3, cols=3, vgap=5, hgap=5)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD)

        size = (100, 100)
        self.button1 = buttons.GenToggleButton(self,id=1, size=size, name="btn1")
        self.button2 = buttons.GenToggleButton(self,id=2, size=size, name="btn2")
        self.button3 = buttons.GenToggleButton(self,id=3, size=size, name="btn3")
        self.button4 = buttons.GenToggleButton(self,id=4, size=size, name="btn4")
        self.button5 = buttons.GenToggleButton(self,id=5, size=size, name="btn5")
        self.button6 = buttons.GenToggleButton(self,id=6, size=size, name="btn6")
        self.button7 = buttons.GenToggleButton(self,id=7, size=size, name="btn7")
        self.button8 = buttons.GenToggleButton(self,id=8, size=size, name="btn8")
        self.button9 = buttons.GenToggleButton(self,id=9, size=size, name="btn9")
        self.normalBtnColour = self.button1.GetBackgroundColour()


        self.widgets = [self.button1, self.button2, self.button3,
                        self.button4, self.button5, self.button6,
                        self.button7, self.button8, self.button9]

        # change all the main game buttons' font and bind them to an event
        for button in self.widgets:
            button.SetFont(font)
            button.Bind(wx.EVT_BUTTON, self.onToggle)

        # add the widgets to the sizers
        self.fgSizer.AddMany(self.widgets)
        mainSizer.Add(self.fgSizer, 0, wx.ALL | wx.CENTER, 5)

        self.titleText = wx.StaticText(self,label='')
        textSizer.Add(self.titleText, 0, wx.CENTER)

        self.endTurnBtn = wx.Button(self, label="DEBUG")
        self.endTurnBtn.Bind(wx.EVT_BUTTON, self.printFlag)
        btnSizer.Add(self.endTurnBtn, 0, wx.ALL | wx.CENTER, 5)

        startOverBtn = wx.Button(self, label="Restart")
        startOverBtn.Bind(wx.EVT_BUTTON, self.onRestart)
        btnSizer.Add(startOverBtn, 0, wx.ALL | wx.CENTER, 5)
        mainSizer.Add(textSizer, 0, wx.CENTER)
        mainSizer.Add(btnSizer, 0, wx.CENTER)

        self.setInitial()



        self.methodsToWin = [(self.button1, self.button2, self.button3),
                             (self.button4, self.button5, self.button6),
                             (self.button7, self.button8, self.button9),
                             # vertical ways to win
                             (self.button1, self.button4, self.button7),
                             (self.button2, self.button5, self.button8),
                             (self.button3, self.button6, self.button9),
                             # diagonal ways to win
                             (self.button1, self.button5, self.button9),
                             (self.button3, self.button5, self.button7)]

        self.SetSizer(mainSizer)

        # Set up event handler for any worker thread results
        EVT_RESULT(self, self.updateDisplay)

    # ----------------------------------------------------------------------
    def onButton(self, event):
        """
        Runs the thread
        """
        # TestThread(self)
        self.displayLbl.SetLabel("Thread started!")
        btn = event.GetEventObject()
        btn.Disable()

    def onToggle(self, event):
        """
        On button toggle, change the label of the button pressed
        and disable the other buttons unless the user changes their mind
        """
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
            self.titleText.SetLabel("WAIT FOR OTHERS")
            for i in range(2):
                time.sleep(1)
            # self.server.setTurn(self.playerId)
            self.server.resetTurn()

            # TestThread(self)
            # self.tretTret.start()
        else:
            print "else"

            # self.endTurnBtn.Disable()

        # check if it's a "cats game" - no one's won
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


    def onRestart(self, event):
        """
        Calls the restart method
        """
        self.server.resetFlag()
        self.restart()
        self.updateView()
    # ----------------------------------------------------------------------
    def printFlag(self, event):
        self.printFlagArr()

    def pyro_client(self):
        uri = "PYRONAME:maile@localhost:7777"
        self.server = Pyro4.Proxy(uri)
        self.server.add_players(self.playerId)


    def setInitial(self):
        self.tretTret.start()
        self.player = self.server.checkIndex(self.playerId)
        print "MY INITIAL IS "+self.player
        if(self.player == 'X'):
            self.Toggled = False
        else:
            # TestThread(self)
            # self.tretTret.join()
            self.titleText.SetLabel("WAIT FOR OTHERS")
            self.Toggled = True
            for btn in self.widgets:
                btn.Disable()



    def printFlagArr(self):
        button_id = self.server.getBtn()
        # print button_id
        decoded = json.loads(button_id)
        for x in decoded:
            print "btn id = "+str(x[0])+" value = "+str(x[1])
            for button in self.widgets:
                if (x[0] == button.GetId()):
                    button.SetLabel(x[1])
                    button.SetValue(True)
                    button.Disable()
        self.checkWin()

    def enableUnusedButtons(self):
        """
        Re-enable unused buttons
        """
        for button in self.widgets:
            if button.GetLabel() == "":
                button.Enable()
        self.Refresh()
        self.Layout()

    def checkWin(self, computer=False):
        """
        Check if the player won
        """
        for button1, button2, button3 in self.methodsToWin:
            if button1.GetLabel() == button2.GetLabel() and \
                    button2.GetLabel() == button3.GetLabel() and \
                    button1.GetLabel() != "":
                # print "Player "+button1.GetLabel()+" wins!"
                self.playerWon = True
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
        button_id = self.server.getBtn()
        # print button_id
        decoded = json.loads(button_id)
        for x in decoded:
            print "btn id = " + str(x[0]) + " value = " + x[1]
            for button in self.widgets:
                if (x[0] == button.GetId()):
                    if(x[1] != ''):
                        button.SetLabel(x[1])
                    button.SetValue(True)
                    button.Disable()

        self.Refresh()
        self.Layout()




    def updateDisplay(self, msg):
        """
        Receives data from thread and updates the display
        """
        t = msg.data
        if isinstance(t, int):
            print "Check your turn"
            self.checkYourTurn(t)
        else:
            print "FINISH"

    def checkYourTurn(self,id):
        # if(id == 999):
        #     print "if 999"
        #     self.server.setTurn(self.playerId)
        if(self.playerId == id):
            print "THIS IS YOUR TURN"
            self.updateView()
            self.titleText.SetLabel("THIS IS YOUR TURN")
            self.Toggled = False
            self.enableUnusedButtons()
        else:
            self.server.setTurn(self.playerId)

# ----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()
