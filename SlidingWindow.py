#!/usr/local/bin/python

# SlidingWindow.py

import wx

class SlidingWindow(wx.Frame):
	
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size = (1000, 800))
		self.topPacketNum = 20
		self.BottomPacketNum = 20
		self.ID_TIMER = 1
		self.windowSize = 5
		self.sendStrategy = "GoBackN"
		self.timeOut = 5
		self.timeCount = 0
		self.speed = 5
		self.fly = []
		self.fly_max = 0
		# self.fly_signal = True
		self.sendingPackets = []
		self.backingPackets = []
		self.initFrame()
	
	def initFrame(self):
		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetStatusText("Status: stop")
		self.timer = wx.Timer(self, self.ID_TIMER)
		self.initController()
		# bind events
		self.Bind(wx.EVT_PAINT, self.drawPacket)
		self.Bind(wx.EVT_TIMER, self.OnTimer, id = self.ID_TIMER)
		self.Bind(wx.EVT_BUTTON, self.OnClick, self.cbtn1)
		self.createPacket()
		# show panel
		self.Centre()
		self.Show(True)
	# click start button
	def OnClick(self, event):
		self.windowSize = self.sc1.GetValue()
		self.speed = 11 - self.sc2.GetValue()
		self.timeOut = self.sc3.GetValue()
		self.timeCount = self.timeOut
		for i in range(self.windowSize):
			self.fly.append(i)
			self.fly_max = i
		self.timer.Start(100)
		self.sc1.Enable(False)
		self.sc2.Enable(False)
		self.sc3.Enable(False)
		self.rb1.Enable(False)
		self.rb2.Enable(False)
		self.statusbar.SetStatusText("Status: start")

	def OnTimer(self, event):
		if event.GetId() == self.ID_TIMER:
			self.sendPacket()
		else:
			event.Skip()
	# change the positions of packets
	def move(self):
		for packet in self.sendingPackets:
			if packet.y <= 700:
				packet.y = packet.y + self.speed
			else:
				self.sendingPackets.remove(packet)
				self.BottomPacket[packet.index].isSent = -1
				self.BottomPacket[packet.index].state = "pink"
		for packet in self.backingPackets:
			if packet.y >= 200:
				packet.y = packet.y - self.speed
			else:
				self.backingPackets.remove(packet)
				self.topPacket[packet.index].isSent = 2
				self.BottomPacket[packet.index].isSent = 2
				self.topPacket[packet.index].state = "yellow"
				if packet.index in self.fly:
					self.fly_max = self.fly_max + 1
					if (self.fly_max + 1) % self.windowSize == 0:
						self.timeCount = self.timeOut
					self.fly.append(self.fly_max)
					self.fly.remove(packet.index)
		self.Refresh()
	# choose what packets to send when Timer is triggered
	def sendPacket(self):
		print(self.timeCount)
		self.timeCount = self.timeCount - 1
		if self.timeCount <= 0:
			self.timeCount = self.timeOut
			if self.sendStrategy == "Selective":
				self.topPacket[i].isSent = 0
			elif self.sendStrategy == "GoBackN":
				for i in self.fly:
					self.topPacket[i].isSent = 0
		for i in range(self.topPacketNum):
			if (i in self.fly) and (self.topPacket[i].isSent == 0):
				print(self.fly)
				self.topPacket[i].isSent = 1
				self.sendingPackets.append(Packet("lightBlue", 20+50*self.topPacket[i].index, 200, self.topPacket[i].index))
		for i in range(self.BottomPacketNum):
			if (i in self.fly) and (self.BottomPacket[i].isSent == -1):
				self.BottomPacket[i].isSent = 1
				self.backingPackets.append(Packet("green", 20+50*self.BottomPacket[i].index, 700, self.BottomPacket[i].index))
		self.move()
	# create packets on the top and bottom of the panel
	def createPacket(self):
		self.topPacket = []
		for i in range(self.topPacketNum):
			self.topPacket.append(Packet("blue", 20+50*i, 200, i))
		self.BottomPacket = []
		for i in range(self.BottomPacketNum):
			self.BottomPacket.append(Packet("white", 20+50*i, 700, i))

	# responsible for draw packets
	def drawPacket(self, event):
		dc = wx.PaintDC(self)
		dc.SetPen(wx.Pen("#d4d4d4"))
		for i in range(self.topPacketNum):
			if self.topPacket[i].state == "blue":
				dc.SetBrush(wx.Brush("#0000ff"))
				dc.DrawCircle(self.topPacket[i].x, self.topPacket[i].y, self.topPacket[i].width)
			elif self.topPacket[i].state == "yellow":
				dc.SetBrush(wx.Brush("#cccc66"))
			dc.DrawCircle(self.topPacket[i].x, self.topPacket[i].y, self.topPacket[i].width)
		for i in range(self.BottomPacketNum):
			if self.BottomPacket[i].state == "white":
				dc.SetBrush(wx.Brush("#a52a2a"))
			elif self.BottomPacket[i].state == "pink":
				dc.SetBrush(wx.Brush("#cc66cc"))
			dc.DrawCircle(self.BottomPacket[i].x, self.BottomPacket[i].y, self.BottomPacket[i].width)
		for i in range(len(self.sendingPackets)):
			dc.SetBrush(wx.Brush("#66cccc"))
			dc.DrawCircle(self.sendingPackets[i].x, self.sendingPackets[i].y, self.sendingPackets[i].width)
		for i in range(len(self.backingPackets)):
			dc.SetBrush(wx.Brush("#cccccc"))
			dc.DrawCircle(self.backingPackets[i].x, self.backingPackets[i].y, self.backingPackets[i].width)

	def initController(self):
		# layout
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.vbox1 = wx.BoxSizer(wx.VERTICAL)
		self.p1 = wx.StaticText(self, label = "Protocol")
		self.vbox1.Add(self.p1, flag = wx.ALL, border = 8)
		self.rb1 = wx.RadioButton(self, label = "Go Back N", style = wx.RB_GROUP)
		self.rb1.SetValue(1)
		self.vbox1.Add(self.rb1, flag = wx.ALL, border = 8)
		self.rb2 = wx.RadioButton(self, label = "Selective Repeat")
		self.vbox1.Add(self.rb2, flag = wx.ALL, border = 8)
		self.hbox.Add(self.vbox1, flag = wx.ALL, border = 25)

		self.vbox2 = wx.BoxSizer(wx.VERTICAL)
		self.p2 = wx.StaticText(self, label = "Window Size")
		self.vbox2.Add(self.p2, flag = wx.ALL, border = 8)
		# self.sld1 = wx.Slider(self, value = 5, minValue = 1, maxValue = 10, style = wx.SL_HORIZONTAL)
		# self.vbox2.Add(self.sld1, flag = wx.ALL, border = 8)
		self.sc1 = wx.SpinCtrl(self, value = '5')
		self.sc1.SetRange(1, 10)
		self.vbox2.Add(self.sc1, flag = wx.ALL, border = 8)
		self.hbox.Add(self.vbox2, flag = wx.ALL, border = 25)

		self.vbox3 = wx.BoxSizer(wx.VERTICAL)
		self.p3 = wx.StaticText(self, label = "End to End Delay")
		self.vbox3.Add(self.p3, flag = wx.ALL, border = 8)
		# self.sld2 = wx.Slider(self, value = 5, minValue = 1, maxValue = 10, style = wx.SL_HORIZONTAL)
		# self.vbox3.Add(self.sld2, flag = wx.ALL, border = 8)
		self.sc2 = wx.SpinCtrl(self, value = '5')
		self.sc2.SetRange(1, 10)
		self.vbox3.Add(self.sc2, flag = wx.ALL, border = 8)
		self.hbox.Add(self.vbox3, flag = wx.ALL, border = 25)

		self.vbox4 = wx.BoxSizer(wx.VERTICAL)
		self.p4 = wx.StaticText(self, label = "Timeout")
		self.vbox4.Add(self.p4, flag = wx.ALL, border = 8)
		# self.sld3 = wx.Slider(self, value = 5, minValue = 1, maxValue = 10, style = wx.SL_HORIZONTAL)
		# self.vbox4.Add(self.sld3, flag = wx.ALL, border = 8)
		self.sc3 = wx.SpinCtrl(self, value = '100')
		self.sc3.SetRange(40, 200)
		self.vbox4.Add(self.sc3, flag = wx.ALL, border = 8)
		self.hbox.Add(self.vbox4, flag = wx.ALL, border = 25)

		self.vbox5 = wx.BoxSizer(wx.VERTICAL)
		self.p5 = wx.StaticText(self, label = "Start")
		self.vbox5.Add(self.p5, flag = wx.ALL, border = 8)
		self.cbtn1 = wx.Button(self, label = "Start")
		self.vbox5.Add(self.cbtn1, flag = wx.ALL, border = 8)
		# self.p6 = wx.StaticText(self, label = "Pause")
		# self.vbox5.Add(self.p6, flag = wx.ALL, border = 8)
		# self.cbtn2 = wx.Button(self, label = "Pause")
		# self.vbox5.Add(self.cbtn2, flag = wx.ALL, border = 8)
		self.hbox.Add(self.vbox5, flag = wx.ALL, border = 25)

		self.SetSizer(self.hbox)

# every packet has its properties
class Packet(object):
	#white: no data received yet
	#blue: data buffered (ready to send, delivered or sent but no ack received yet)
	#green: ack
	#yellow: transmission confirmed
	#purple: data has been delivered to upper network layer
	#lightblue: sending packet
	def __init__(self, state, x, y, index):
		self.state = state
		self.x = x
		self.y = y
		self.width = 15
		self.isSent = 0
		self.index = index

# program starts
app = wx.App()
SlidingWindow(None, title = "Sliding Window")
app.MainLoop()