import os
import time
import json
import board
import busio
import usb_hid
import rotaryio
import digitalio
import displayio
import terminalio
import adafruit_displayio_sh1106
from adafruit_display_text import label
from adafruit_debouncer import Debouncer
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from minikbd import MiniKbdButtons


def divideListIntoUIChunks(l):
	div_l = []
	overlappedList = False
	for i, ch in enumerate(l):

		if i+1 < len(l):
			next_ch = l[i+1]
		else:
			next_ch = next_ch = l[0]

		if i+2 < len(l):
			next_next_ch = l[i+2]
		else:
			if not overlappedList:
				next_next_ch = l[0]
				overlappedList = True
			else:
				next_next_ch = l[1]
		div_l.append((ch, next_ch, next_next_ch))

	return div_l


def initOptions():
	configDir = os.listdir("configs")
	optionsDict = {}
	for file in configDir:
		if file.startswith("."): continue
		if file.split(".")[-1] != "json": continue
		path = f"configs/{file}"
		with open(path,"r") as f:
			json_txt = f.read()
			mappingDict = json.loads(json_txt)
			mappingDict["path"] = path
			shortcuts = []

			for shortcutSet in mappingDict['shortcuts']:
				shortcutSetObj = [getattr(Keycode, name) for name in shortcutSet]
				shortcuts.append(shortcutSetObj)
			mappingDict['shortcuts'] = shortcuts

			wheels = {}

			for wheelTitle, wheelset in mappingDict['wheels'].items():
				if len(wheelset) == 2:
					wheelLeft, wheelRight = wheelset
					wheelLeftObj = [getattr(Keycode, name) for name in wheelLeft]
					wheelRightObj = [getattr(Keycode, name) for name in wheelRight]
					wheels[wheelTitle] = wheelLeftObj, wheelRightObj
				else:
					wheelShortcuts = []
					for wheelShortcut in wheelset:
						wheelObjs = [getattr(Keycode, name) for name in wheelShortcut]
						wheelShortcuts.append(wheelObjs)
					wheels[wheelTitle] = wheelShortcuts
			mappingDict['wheels'] = wheels
			if "cache" not in mappingDict.keys():
				mappingDict["cache"] = {}
			
			optionsDict[file[:-5]] = mappingDict

	return optionsDict


class Encoder:
	last_position = 0
	def __init__(self, pin1, pin2, upCallback=None, downCallback=None):
		self.encoder = rotaryio.IncrementalEncoder(pin1, pin2)
		self.upCallback = upCallback
		self.downCallback = downCallback
	
	def setUpCallback(self, upCallback):
		self.upCallback = upCallback
	
	def setDownCallback(self, downCallback):
		self.downCallback = downCallback

	def update(self):
		position = self.encoder.position
			
		if position > self.last_position:
			if self.upCallback is not None: self.upCallback()
		if position < self.last_position:
			if self.downCallback is not None: self.downCallback()
		self.last_position = position


class MacroPadUI:
	last_position = 0
	_allowWheelConfChange = False
	_allowWheelConfChange_Last = False
	shortcutList = None
	enc1CarouselIndex = 0
	enc2CarouselIndex = 0
	def __init__(self, 
					sda="GP8", scl="GP9", 
					A1pin="GP3", B1pin="GP2", 
					wheelSwitchPin1="GP15", 
					A2pin="GP5", B2pin="GP4", 
					wheelSwitchPin2="GP1", 
					allowWheelConfChangeSwitchPin="GP0"
				):
		self.kbd = Keyboard(usb_hid.devices)
		self.buttonMatrix = MiniKbdButtons(
									keyDownCallback=self.buttonDownCallback, 
									keyUpCallback=self.buttonUpCallback
									)
		self.optionsDict = initOptions()
		
		self.optionSetNames = list(self.optionsDict.keys())
		self._optionSetUiChunks = divideListIntoUIChunks(range(len(self.optionSetNames)))
		self.optionCount = len(self.optionSetNames)
		
		self.avaibleWheelOptions = []
		self.selection = 0
		self._uiSelection = 0 # 0 = top, 1 = middle, 2 = bottom
		self._last_uiSelection = self._uiSelection
		self._uiChunkIndex = 0
		self._currentChunk = 0
		self.wheelSelection1 = 0
		self.wheelSelection2 = 1 # self.getDefaultEn2()
		self.currentOptionName = self.optionSetNames[self.selection]
		self.frozen_encoder_position = None

		self.updateGUI()
		self.setWheelOptions()
		self.initDisplay(sda, scl, A1pin, B1pin, A2pin, B2pin, wheelSwitchPin1, wheelSwitchPin2, allowWheelConfChangeSwitchPin)
		self.updateOptionSet()

	# def getDefaultEn2(self):
	# 	return len(self.avaibleWheelOptions) - 1

	def setEn1Cache(self, value):
		self.optionsDict[self.currentOptionName]["cache"]["en1"] = value

	def setEn2Cache(self, value):
		self.optionsDict[self.currentOptionName]["cache"]["en2"] = value

	def getEn1Cache(self):
		value = self.optionsDict[self.currentOptionName]["cache"].get("en1")
		if value is None:
			value = 0
		return value

	def getEn2Cache(self):
		value = self.optionsDict[self.currentOptionName]["cache"].get("en2")
		if value is None:
			value = 1 # self.getDefaultEn2()
		return value

	def saveCache(self):
		self.setEn1Cache(self.wheelSelection1)
		self.setEn2Cache(self.wheelSelection2)


	def loadCache(self):
		self.wheelSelection1 = 0
		en1CachedValue = self.getEn1Cache()
		
		if en1CachedValue < len(self.avaibleWheelOptions):
			self.wheelSelection1 = en1CachedValue

		self.wheelSelection2 = 1 # self.getDefaultEn2()
		en2CachedValue = self.getEn2Cache()
		
		if en2CachedValue < len(self.avaibleWheelOptions):
			self.wheelSelection2 = en2CachedValue



	def initDisplay(self, sda, scl, A1pin, B1pin, A2pin, B2pin, wheelSwitchPin1, wheelSwitchPin2, allowWheelConfChangeSwitchPin):
		wheelSwitchPin1 = digitalio.DigitalInOut(getattr(board, wheelSwitchPin1))
		wheelSwitchPin1.direction = digitalio.Direction.INPUT
		wheelSwitchPin1.pull = digitalio.Pull.UP
		self.wheelSwitch1 = Debouncer(wheelSwitchPin1)

		wheelSwitchPin2 = digitalio.DigitalInOut(getattr(board, wheelSwitchPin2))
		wheelSwitchPin2.direction = digitalio.Direction.INPUT
		wheelSwitchPin2.pull = digitalio.Pull.UP
		self.wheelSwitch2 = Debouncer(wheelSwitchPin2)

		allowWheelConfChangeSwitchPin = digitalio.DigitalInOut(getattr(board,allowWheelConfChangeSwitchPin))
		allowWheelConfChangeSwitchPin.direction = digitalio.Direction.INPUT
		allowWheelConfChangeSwitchPin.pull = digitalio.Pull.UP
		self.allowWheelConfChangeSwitch = Debouncer(allowWheelConfChangeSwitchPin)

		A = getattr(board,A1pin)
		B = getattr(board,B1pin)
		self.encoder1 = Encoder(A, B, self._en1UpCallback, self._en1DownCallback)

		A = getattr(board,A2pin)
		B = getattr(board,B2pin)
		self.encoder2 = Encoder(A, B, self._en2UpCallback, self._en2DownCallback)

		displayio.release_displays()
		SDA = getattr(board,sda)
		SCL = getattr(board,scl)
		i2c = busio.I2C(SCL, SDA, frequency=400000)
		i2c_bus = displayio.I2CDisplay(i2c, device_address=60)
		WIDTH = 132
		HEIGHT = 64
		BORDER = 10
		display = adafruit_displayio_sh1106.SH1106(i2c_bus, width=WIDTH, height=HEIGHT)
		bitmap = displayio.OnDiskBitmap("/logo.bmp")
		tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
		splash = displayio.Group()
		splash.append(tile_grid)
		display.show(splash)
	
		time.sleep(1.5)
		splash.remove(tile_grid)

		text_group = displayio.Group(scale=1, x=10, y=4)
		txt = self.getDisplayText()
		self.text_area = label.Label(terminalio.FONT, text=txt, color=0xFFFF00)
		text_group.append(self.text_area)
		splash.append(text_group)

	def buttonDownCallback(self, buttonID, othersDown):
		self.kbd.press(*self.shortcutList[buttonID-1])
		print("btn _down_", buttonID, othersDown)

	def buttonUpCallback(self, buttonID):
		self.kbd.release(*self.shortcutList[buttonID-1])
		print("btn ^UPUP^", buttonID)

	def updateAllowWheel(self):
		self.allowWheelConfChangeSwitch.update()
		if self.allowWheelConfChangeSwitch.fell:
			self._allowWheelConfChange = True
			self.saveCache()
			self.updateOptionSet()

		if self.allowWheelConfChangeSwitch.rose:
			self._allowWheelConfChange = False
			self.updateOptionSet()

	def update(self):
		self.updateAllowWheel()
		self.updateSwitchWheel()
		self.encoder1.update()
		self.encoder2.update()
		self.buttonMatrix.update()
			
	def _en1UpCallback(self):
		print("en1 UP")
		# select config mode
		if self._allowWheelConfChange:
			self.selectNext()
			self.updateOptionSet()
		else:
			self.en1ActionUp()

	def _en1DownCallback(self):
		print("en1 DOWN")
		# select config mode
		if self._allowWheelConfChange:
			self.selectPrev()
			self.updateOptionSet()
		else:
			self.en1ActionDown()

	def _en2UpCallback(self):
		print("en2 UP")
		# select config mode
		if self._allowWheelConfChange:
			pass
		else:
			self.en2ActionUp()

	def _en2DownCallback(self):
		print("en2 DOWN")
		# select config mode
		if self._allowWheelConfChange:
			pass
		else:
			self.en2ActionDown()
	
	def en1ActionUp(self):
		if self.isEnc1LeftRight:
			self.kbd.press(*self.enc1Actions[0])
			self.kbd.release(*self.enc1Actions[0])
		else:
			self.kbd.press(*self.enc1Actions[self.enc1CarouselIndex])
			self.kbd.release(*self.enc1Actions[self.enc1CarouselIndex])
			self.enc1CarouselIndex -= 1
			if self.enc1CarouselIndex == -1:
				self.enc1CarouselIndex = self.enc1ListLength-1

	def en1ActionDown(self):
		if self.isEnc1LeftRight:
			self.kbd.press(*self.enc1Actions[1])
			self.kbd.release(*self.enc1Actions[1])
		else:
			self.kbd.press(*self.enc1Actions[self.enc1CarouselIndex])
			self.kbd.release(*self.enc1Actions[self.enc1CarouselIndex])
			self.enc1CarouselIndex += 1
			if self.enc1CarouselIndex == self.enc1ListLength:
				self.enc1CarouselIndex = 0
		

	def en2ActionUp(self):
		if self.isEnc2LeftRight:
			self.kbd.press(*self.enc2Actions[0])
			self.kbd.release(*self.enc2Actions[0])
		else:
			self.kbd.press(*self.enc2Actions[self.enc2CarouselIndex])
			self.kbd.release(*self.enc2Actions[self.enc2CarouselIndex])
			self.enc2CarouselIndex -= 1
			if self.enc2CarouselIndex == -1:
				self.enc2CarouselIndex = self.enc2ListLength-1
		
	def en2ActionDown(self):
		if self.isEnc2LeftRight:
			self.kbd.press(*self.enc2Actions[1])
			self.kbd.release(*self.enc2Actions[1])
		else:
			self.kbd.press(*self.enc2Actions[self.enc2CarouselIndex])
			self.kbd.release(*self.enc2Actions[self.enc2CarouselIndex])
			self.enc2CarouselIndex += 1
			if self.enc2CarouselIndex == self.enc2ListLength:
				self.enc2CarouselIndex = 0

	def updateSwitchWheel(self):
		self.wheelSwitch1.update()
		if self.wheelSwitch1.fell:
			wheelSelection = self.wheelSelection1
			wheelSelection += 1
			if wheelSelection == len(self.avaibleWheelOptions):
				wheelSelection = 0
			self.wheelSelection1 = wheelSelection
			self.setWheelOptions()
			self.updateText()


		self.wheelSwitch2.update()
		if self.wheelSwitch2.fell:
			wheelSelection = self.wheelSelection2
			wheelSelection += 1
			if wheelSelection == len(self.avaibleWheelOptions):
				wheelSelection = 0
			self.wheelSelection2 = wheelSelection
			self.setWheelOptions()
			self.updateText()

		
	def updateGUI(self):
		currentChunk = self._optionSetUiChunks[self._uiChunkIndex]
		top, mid, bot = [self.optionSetNames[i] for i in currentChunk]
		self.setTop(top)
		self.setMiddle(mid)
		self.setBottom(bot)

	def updateOptionSet(self):
		self.shortcutList = self.optionsDict[self.currentOptionName]['shortcuts']
		# self.cacheDict = self.optionsDict[self.currentOptionName]["cache"]

		self.loadCache()

		self.updateGUI()
		self.currentOptionName = self.optionSetNames[self.selection]
		self.setWheelOptions()
		self.updateText()

	def setWheelOptions(self):
		print("setWheelOptions")
		self.avaibleWheelOptions = list(self.optionsDict[self.currentOptionName]['wheels'].keys())
		
		if self.wheelSelection1 >= len(self.avaibleWheelOptions):
			self.wheelSelection1 = 0
		self.setWheel1txt(self.avaibleWheelOptions[self.wheelSelection1])
		self.enc1Actions = self.optionsDict[self.currentOptionName]['wheels'][self.getWheel1txt()]

		if self.wheelSelection2 >= len(self.avaibleWheelOptions):
			self.wheelSelection2 = 0
		self.setWheel2txt(self.avaibleWheelOptions[self.wheelSelection2])
		self.enc2Actions = self.optionsDict[self.currentOptionName]['wheels'][self.getWheel2txt()]
		

		self.enc1ListLength = len(self.enc1Actions)
		self.isEnc1LeftRight = False
		self.enc1CarouselIndex = 0
		if self.enc1ListLength == 2:
			self.isEnc1LeftRight = True
		
		self.enc2ListLength = len(self.enc2Actions)
		self.isEnc2LeftRight = False
		self.enc2CarouselIndex = 0
		if self.enc2ListLength == 2:
			self.isEnc2LeftRight = True

	def updateText(self):
		self._currentChunk = None###
		txt = self.getDisplayText()
		self.text_area.text = txt

	def selectNext(self):
		selection = self.selection + 1
		if selection == self.optionCount:
			self.selection = 0
		else:
			self.selection = selection

		self._last_uiSelection = self._uiSelection
		
		if not self._uiSelection + 1 > 2:
			self._uiSelection += 1
		if self._last_uiSelection == self._uiSelection:
			self._uiChunkIndex += 1
			if self._uiChunkIndex + 0 == len(self._optionSetUiChunks):
				self._uiChunkIndex = 0

	def selectPrev(self):
		selection = self.selection - 1
		if selection < 0:
			self.selection = self.optionCount-1
		else:
			self.selection = selection
		
		self._last_uiSelection = self._uiSelection
		
		if not self._uiSelection - 1 < 0:
			self._uiSelection -= 1
		if self._last_uiSelection == self._uiSelection:
			if self._uiChunkIndex - 1 < 0:
				self._uiChunkIndex = len(self._optionSetUiChunks)
			self._uiChunkIndex -= 1

	def setTop(self, value):
		self._top = value

	def getTop(self):
		txt = self._top
		if self._uiSelection == 0:
			txt = " > " + txt
		return txt

	def setMiddle(self, value):
		self._middle = value

	def getMiddle(self):
		txt = self._middle
		if self._uiSelection == 1:
			txt = " > " + txt
		return txt

	def setBottom(self, value):
		self._bottom = value

	def getBottom(self):
		txt = self._bottom
		if self._uiSelection == 2:
			txt = " > " + txt
		return txt

	def setWheel1txt(self, value):
		self._wheel1 = value

	def getWheel1txt(self):
		return self._wheel1

	def setWheel2txt(self, value):
		self._wheel2 = value

	def getWheel2txt(self):
		return self._wheel2

	def getDisplayText(self):
		if self._allowWheelConfChange:
			return f"Preset selection:\n{self.getTop()}\n{self.getMiddle()}\n{self.getBottom()}"
		else:
			return f"{self.currentOptionName}\n-------------------\ne1:{self.getWheel1txt()}\ne2:{self.getWheel2txt()}"

	# def sleep(self):
	#     pass

	# def wake(self):
	#     pass


#