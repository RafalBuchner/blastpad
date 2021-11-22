import board
from digitalio import DigitalInOut, Direction, Pull

ROW0 = "GP16"
ROW1 = "GP17"
ROW2 = "GP18"
ROW3 = "GP19"
ROW4 = "GP20"

COL0 = "GP21"
COL1 = "GP22"
COL2 = "GP26"
COL3 = "GP27"
COL4 = "GP28"

COLS = [
	COL0, COL1, COL2, COL3, COL4
]

ROWS = [
	ROW0, ROW1, ROW2, ROW3, ROW4
]
class MiniKbdButtons:
	
	def __init__(self, keyDownCallback=None, keyUpCallback=None,):
		# Callbacks
		self.downCback = keyDownCallback
		self.upCback = keyUpCallback
		# Button state and map
		self.state = []
		self.pins = {}
		self.btnMap = [
			dict(row=ROW4, col=COL0, id=1), #
			dict(row=ROW4, col=COL1, id=2),
			dict(row=ROW4, col=COL2, id=3),
			dict(row=ROW4, col=COL3, id=4),
			dict(row=ROW4, col=COL4, id=5),
			dict(row=ROW3, col=COL0, id=6), #
			dict(row=ROW3, col=COL1, id=7),
			dict(row=ROW3, col=COL2, id=8),
			dict(row=ROW3, col=COL3, id=9),
			dict(row=ROW3, col=COL4, id=10),
			dict(row=ROW2, col=COL0, id=11), #
			dict(row=ROW2, col=COL1, id=12),
			dict(row=ROW2, col=COL2, id=13),
			dict(row=ROW2, col=COL3, id=14),
			dict(row=ROW2, col=COL4, id=15),
			dict(row=ROW1, col=COL1, id=16), #
			dict(row=ROW1, col=COL2, id=17),
			dict(row=ROW1, col=COL3, id=18),
			dict(row=ROW1, col=COL4, id=19),
			dict(row=ROW0, col=COL0, id=20), #
			dict(row=ROW0, col=COL1, id=21),
			dict(row=ROW0, col=COL2, id=22),
			dict(row=ROW0, col=COL4, id=23)]
		self.initPins()
	
	def initPins(self):
		# Rows
		for pn in ROWS:
			p = DigitalInOut(getattr(board, pn))
			p.direction = Direction.OUTPUT
			self.pins[pn] = p
		# Columns
		for pn in COLS:
			p = DigitalInOut(getattr(board, pn))
			p.direction = Direction.INPUT
			p.pull = Pull.DOWN
			self.pins[pn] = p
	
	def update(self):
		# Compare old and new state
		oldSt = self.state
		newSt = []
		newBtn = None
		for btn in self.btnMap:
			r = self.pins[btn["row"]]
			r.value = True
			if self.pins[btn["col"]].value:
				newSt += [btn["id"]]
				if not btn["id"] in oldSt:
					newBtn = btn["id"]
			r.value = False
		# Callbacks
		for oID in oldSt:
			if not oID in newSt:
				self.upCback(oID)
		if newBtn:
			self.downCback(newBtn, newSt)
		self.state = newSt