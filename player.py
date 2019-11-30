import random
import Pyro4
import wx
import os,sys
import wx.lib.buttons as buttons
 
########################################################################
class TTTPanel(wx.Panel):
    """
    Tic-Tac-Toe Panel object
    """
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """
        Initialize the panel
        """
        wx.Panel.__init__(self, parent)
        self.oToggled = False
        self.xToggled = False
        self.playerWon = False
        self.player = 'X'
        self.font = ''
        self.server = ''
 
        self.layoutWidgets()
        self.pyro_client()

    #----------------------------------------------------------------------

    
    def pyro_client(self):
        uri = "PYRONAME:maile@localhost:7777"
        self.server = Pyro4.Proxy(uri)


    def writeLog(self,data):
        fd = open("log.txt","w+")
        fd.write(data)
        fd.close()    
 
    #----------------------------------------------------------------------
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
                    msg = "Selamat Player "+button1.GetLabel()+" menang! main lagi?"
                    dlg = wx.MessageDialog(None, msg, "Winner!",
                                           wx.YES_NO | wx.ICON_WARNING)
                    result = dlg.ShowModal()
                    if result == wx.ID_YES:
                        wx.CallAfter(self.restart)
                    dlg.Destroy()
                    break
                else:
                    return True
 
    #----------------------------------------------------------------------
    def layoutWidgets(self):
        """
        Create and layout the widgets
        """
        print "sini"
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.fgSizer = wx.FlexGridSizer(rows=3, cols=3, vgap=5, hgap=5)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD)
 
        size = (100,100)
        self.button1 = buttons.GenToggleButton(self, size=size, name="btn1")
        self.button2 = buttons.GenToggleButton(self, size=size, name="btn2")
        self.button3 = buttons.GenToggleButton(self, size=size, name="btn3")
        self.button4 = buttons.GenToggleButton(self, size=size, name="btn4")
        self.button5 = buttons.GenToggleButton(self, size=size, name="btn5")
        self.button6 = buttons.GenToggleButton(self, size=size, name="btn6")
        self.button7 = buttons.GenToggleButton(self, size=size, name="btn7")
        self.button8 = buttons.GenToggleButton(self, size=size, name="btn8")
        self.button9 = buttons.GenToggleButton(self, size=size, name="btn9")
        self.normalBtnColour = self.button1.GetBackgroundColour()
 
        self.widgets = [self.button1, self.button2, self.button3,
                        self.button4, self.button5, self.button6, 
                        self.button7, self.button8, self.button9]
 
        # change all the main game buttons' font and bind them to an event
        for button in self.widgets:
            button.SetFont(font)
            button.Bind(wx.EVT_BUTTON, self.onToggleX)
 
        # add the widgets to the sizers
        self.fgSizer.AddMany(self.widgets)
        mainSizer.Add(self.fgSizer, 0, wx.ALL|wx.CENTER, 5)
 
        # self.endTurnBtn = wx.Button(self, label="End Turn")
        # self.endTurnBtn.Bind(wx.EVT_BUTTON, self.onEndTurn)
        # btnSizer.Add(self.endTurnBtn, 0, wx.ALL|wx.CENTER, 5)
         
        startOverBtn = wx.Button(self, label="Restart")
        startOverBtn.Bind(wx.EVT_BUTTON, self.onRestart)
        btnSizer.Add(startOverBtn, 0, wx.ALL|wx.CENTER, 5)
        mainSizer.Add(btnSizer, 0, wx.CENTER)
 
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
    #----------------------------------------------------------------------
    def switchToX(self):
        print "to X"
        for button in self.widgets:
            button.Bind(wx.EVT_BUTTON, self.onToggleX)        

    #----------------------------------------------------------------------
    def switchToO(self):
        print "to O"
        for button in self.widgets:
            button.Bind(wx.EVT_BUTTON, self.onToggleO)        

    #----------------------------------------------------------------------
    def switch(self):
        print self.player
        if(self.player == 'X'):
            self.xToggled = False
            self.switchToO()
            self.player = 'O'

        elif(self.player == 'O'):
            self.oToggled = False
            self.switchToX()
            self.player = 'X'

        self.enableUnusedButtons()
            
    #----------------------------------------------------------------------
    def enableUnusedButtons(self):
        """
        Re-enable unused buttons
        """
        for button in self.widgets:
            if button.GetLabel() == "":
                button.Enable()
        self.Refresh()
        self.Layout()
 
    #----------------------------------------------------------------------
    def onEndTurn(self, event):
        self.switch()
    #----------------------------------------------------------------------
    def giveUp(self):
        """
        The computer cannot find a way to play that lets the user win,
        so it gives up.
        """
        msg = "Draw..."
        dlg = wx.MessageDialog(None, msg, "Game Over!",
                               wx.YES_NO | wx.ICON_WARNING)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.restart()
        else:
            wx.CallAfter(self.GetParent().Close)
        dlg.Destroy()          
 
    #----------------------------------------------------------------------
    def onRestart(self, event):
        """
        Calls the restart method
        """
        self.testSetBtn()
 
    #----------------------------------------------------------------------
    def onToggleX(self, event):
        """
        On button toggle, change the label of the button pressed
        and disable the other buttons unless the user changes their mind
        """
        button = event.GetEventObject()
        button.SetLabel("X")
        button_id = button.GetId()

        print self.server.setBtn(str(button_id))
 
        self.checkWin()
        if not self.xToggled:
            self.xToggled = True
            # self.endTurnBtn.Enable()
            for btn in self.widgets:
                if button_id != btn.GetId():
                    btn.Disable()
        else:
            self.xToggled = False
            # self.endTurnBtn.Disable()
            button.SetLabel("")
            self.enableUnusedButtons()
 
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

        self.switch()
    
    #----------------------------------------------------------------------
    def onToggleO(self, event):
        """
        On button toggle, change the label of the button pressed
        and disable the other buttons unless the user changes their mind
        """
        
        button = event.GetEventObject()
        button.SetLabel("O")
        button_id = button.GetId()

        print self.server.setBtn(str(button_id))
 
        self.checkWin()
        if not self.oToggled:
            self.oToggled = True
            # self.endTurnBtn.Enable()
            for btn in self.widgets:
                if button_id != btn.GetId(): 
                    btn.Disable()
        else:
            self.oToggled = False
            # self.endTurnBtn.Disable()
            button.SetLabel("")
            self.enableUnusedButtons()
 
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

        self.switch()
    #----------------------------------------------------------------------
    def restart(self):
        """
        Restart the game and reset everything
        """
        for button in self.widgets:
            button.SetLabel("")
            button.SetValue(False)
            button.SetBackgroundColour(self.normalBtnColour)
        self.toggled = False
        self.playerWon = False
        # self.endTurnBtn.Disable()
        self.enableUnusedButtons()        
    #---------------------------------------------------------------------
    def testSetBtn(self):
        """
        Restart the game and reset everything
        """
        button_id = self.server.getBtn()
        
        print button_id

        for button in self.widgets:
            if(button_id == button.GetId()):
                button.SetLabel("W")
                button.SetValue(True)
                button.Disable()

        
        
        
        # for button in self.widgets:
        #     button.SetLabel("")
        #     button.SetValue(False)
        #     button.SetBackgroundColour(self.normalBtnColour)
        # self.toggled = False
        # self.playerWon = False
        # # self.endTurnBtn.Disable()
        # self.enableUnusedButtons() 

########################################################################
class TTTFrame(wx.Frame):
    """
    Tic-Tac-Toe Frame object
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        title = "Tic-Tac-Toe"
        size = (500, 500)
        wx.Frame.__init__(self, parent=None, title=title, size=size)
        panel = TTTPanel(self)
 
        self.Show()




 
if __name__ == "__main__":
    app = wx.App(False)
    frame = TTTFrame()
    app.MainLoop()
    