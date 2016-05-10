#!/usr/local/bin/python

# FlowControl.py

import wx
import random

class FlowControl(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (500, 400))
        self.initFrame()

    def initFrame(self):
        # layout
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.p1 = wx.StaticText(self, label = "L: send file (byte); R: receiver buffer (byte)")

        self.sendfilesize = wx.SpinCtrl(self, value = '2048')
        self.sendfilesize.SetRange(1, 4096)
        self.hbox1.Add(self.sendfilesize, flag = wx.ALL, border = 4)
        self.recebuffer = wx.SpinCtrl(self, value = '1024')
        self.recebuffer.SetRange(1, 2048)
        self.hbox1.Add(self.recebuffer, flag = wx.ALL, border = 4)

        self.p2 = wx.StaticText(self, label = "L: data in sender buffer (= 256 byte); R: data in receiver buffer")

        # sender buffer = 100, receiver buffer = 100
        self.gsendbuffer = wx.Gauge(self, 0, 100, (10, 30), (170, 30))
        self.grecebuffer = wx.Gauge(self, 0, 100, (180, 30), (200, 30))
        self.hbox2.Add(self.gsendbuffer, flag = wx.ALL, border = 4)
        self.hbox2.Add(self.grecebuffer, flag = wx.ALL, border = 4)

        self.p3 = wx.StaticText(self, label = "L: sending process (%); R: receiving process (%)")

        self.gsendprocess = wx.Gauge(self, 0, 100, (10, 110), (170, 110))
        self.greceprocess = wx.Gauge(self, 0, 100, (180, 110), (200, 110))
        self.hbox3.Add(self.gsendprocess, flag = wx.ALL, border = 4)
        self.hbox3.Add(self.greceprocess, flag = wx.ALL, border = 4)

        self.vbox.Add(self.p1, flag = wx.ALL, border = 4)
        self.vbox.Add(self.hbox1, flag = wx.ALL, border = 4)
        self.vbox.Add(self.p2, flag = wx.ALL, border = 4)
        self.vbox.Add(self.hbox2, flag = wx.ALL, border = 4)
        self.vbox.Add(self.p3, flag = wx.ALL, border = 4)
        self.vbox.Add(self.hbox3, flag = wx.ALL, border = 4)

        self.cbtn = wx.Button(self, label = "Start")
        self.vbox.Add(self.cbtn, flag = wx.ALL, border = 4)

        self.SetSizer(self.vbox)

        # show panel
        self.Centre()
        self.Show(True)
        # bind events
        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.cbtn)
    # click start
    def OnClick(self, event):
        # initial widgets
        self.gsendbuffer.SetValue(0)
        self.grecebuffer.SetValue(0)
        self.gsendprocess.SetValue(100)
        self.greceprocess.SetValue(0)
        self.totalfile = self.sendfilesize.GetValue()
        self.totalsendingfile = self.totalfile
        self.receivebuffersize = self.recebuffer.GetValue()
        self.sendbuffersize = 256
        self.dataInreceivebuffer = 0
        self.dataInsendbuffer = 0
        # time interval = 1000 ms
        self.timer.Start(1000)
        self.sendfilesize.Enable(False)
        self.recebuffer.Enable(False)
        self.sendcount = 0
        self.receivecount = 0

    def TimerHandler(self, event):
        # app at receiver consume packets at random
        canreceive = random.randint(1, 300)
        # sender
        if self.totalsendingfile >= 256 - self.dataInsendbuffer:
            self.totalsendingfile = self.totalsendingfile - (256 - self.dataInsendbuffer)
            self.dataInsendbuffer = self.sendbuffersize
        else:
            self.dataInsendbuffer = self.dataInsendbuffer + self.totalsendingfile
            self.totalsendingfile = 0
        # change the value of number of data in send buffer
        self.gsendbuffer.SetValue(self.dataInsendbuffer*100/self.sendbuffersize)
        # receiver
        if self.dataInsendbuffer >= self.receivebuffersize - self.dataInreceivebuffer:
            self.sendcount = self.sendcount + (self.receivebuffersize - self.dataInreceivebuffer)
            self.dataInsendbuffer = self.dataInsendbuffer - (self.receivebuffersize - self.dataInreceivebuffer)
            self.dataInreceivebuffer = self.receivebuffersize
        else:
            self.sendcount = self.sendcount + self.dataInsendbuffer
            self.dataInreceivebuffer = self.dataInreceivebuffer + self.dataInsendbuffer
            self.dataInsendbuffer = 0
        # consume packets
        if canreceive >= self.dataInreceivebuffer:
            self.receivecount = self.receivecount + self.dataInreceivebuffer
            self.dataInreceivebuffer = 0
        else:
            self.receivecount = self.receivecount + canreceive
            self.dataInreceivebuffer = self.dataInreceivebuffer - canreceive
        # change the values of widgets
        self.gsendprocess.SetValue((self.totalfile-self.sendcount)*100/self.totalfile)
        self.grecebuffer.SetValue(self.dataInreceivebuffer*100/self.receivebuffersize)
        self.greceprocess.SetValue(self.receivecount*100/self.totalfile)

# program starts
app = wx.App()
FlowControl(None, title = "Flow Control")
app.MainLoop()