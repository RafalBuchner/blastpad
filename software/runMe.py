import sys
import json
# from PyQt5.QtCore import Qt, QSize
# from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QWidget, QPushButton

from layout_colorwidget import Color
from PyQt5 import QtCore, QtGui, QtWidgets

QT_CONVERSION = {
        "Meta":"Control",
        "Ctrl":"Command",
        "Alt":"Option",
        "Esc":"Escape",
        "Del":"Delete",
    }

QT_TO_ADAFRUIT = {
    "1":"ONE",
    "2":"TWO",
    "3":"THREE",
    "4":"FOUR",
    "5":"FIVE",
    "6":"SIX",
    "7":"SEVEN",
    "8":"EIGHT",
    "9":"NINE",
    "0":"ZERO",
    "Enter":"ENTER",
    "Return":"RETURN",
    "Escape":"ESCAPE",
    "Backspace":"BACKSPACE",
    "Tab":"TAB",
    "Space":"SPACEBAR",
    # "Space":"SPACE",
    "-":"MINUS",
    "=":"EQUALS",
    "[":"LEFT_BRACKET",
    "]":"RIGHT_BRACKET",
    "\\":"BACKSLASH",
    "Pound":"POUND", # extra
    ";":"SEMICOLON",
    "'":"QUOTE",
    "`":"GRAVE_ACCENT",
    ",":"COMMA",
    ".":"PERIOD",
    "/":"FORWARD_SLASH",

    "CapsLock":"CAPS_LOCK", # extra

    "F1":"F1", # extra
    "F2":"F2", # extra
    "F3":"F3", # extra
    "F4":"F4", # extra
    "F5":"F5", # extra
    "F6":"F6", # extra
    "F7":"F7", # extra
    "F8":"F8", # extra
    "F9":"F9", # extra
    "F10":"F10", # extra
    "F11":"F11", # extra
    "F12":"F12", # extra

    "PrintScreen":"PRINT_SCREEN", # extra
    "ScrollLock":"SCROLL_LOCK", # extra
    "Pause":"PAUSE", # extra

    "Insert":"INSERT", # extra
    "Home":"HOME", # extra
    "PgUp":"PAGE_UP", # extra
    "Delete":"DELETE", # extra
    "End":"END", # extra
    "PgDown":"PAGE_DOWN", # extra

    "Right":"RIGHT_ARROW", # extra
    "Left":"LEFT_ARROW", # extra
    "Down":"DOWN_ARROW", # extra
    "Up":"UP_ARROW", # extra

    "Keypad_Numlock":"KEYPAD_NUMLOCK", # extra
    "Keypad_Slash":"KEYPAD_FORWARD_SLASH", # extra
    "Keypad_Asterisk":"KEYPAD_ASTERISK", # extra
    "Keypad_Minus":"KEYPAD_MINUS", # extra
    "Keypad_Plus":"KEYPAD_PLUS", # extra
    "Keypad_Enter":"KEYPAD_ENTER", # extra
    "Keypad_One":"KEYPAD_ONE", # extra
    "Keypad_Two":"KEYPAD_TWO", # extra
    "Keypad_Three":"KEYPAD_THREE", # extra
    "Keypad_Four":"KEYPAD_FOUR", # extra
    "Keypad_Five":"KEYPAD_FIVE", # extra
    "Keypad_Six":"KEYPAD_SIX", # extra
    "Keypad_Seven":"KEYPAD_SEVEN", # extra
    "Keypad_Eight":"KEYPAD_EIGHT", # extra
    "Keypad_Nine":"KEYPAD_NINE", # extra
    "Keypad_Zero":"KEYPAD_ZERO", # extra
    "Keypad_Period":"KEYPAD_PERIOD", # extra
    "Keypad_Backslash":"KEYPAD_BACKSLASH", # extra

    "Application":"APPLICATION", # extra
    "Power":"POWER", # extra
    "Keypad_Equals":"KEYPAD_EQUALS", # extra
    "F13":"F13", # extra
    "F14":"F14", # extra
    "F15":"F15", # extra
    "F16":"F16", # extra
    "F17":"F17", # extra
    "F18":"F18", # extra
    "F19":"F19", # extra

    "F20":"F20", # extra
    "F21":"F21", # extra
    "F22":"F22", # extra
    "F23":"F23", # extra
    "F24":"F24", # extra

    "Left_Control":"LEFT_CONTROL", # extra
    "Control":"CONTROL", # extra
    "Left_Shift":"LEFT_SHIFT", # extra
    "Shift":"SHIFT", # extra
    "Left_Alt":"LEFT_ALT", # extra
    "Alt":"ALT", # extra
    "Option":"OPTION", # extra
    "Left_Gui":"LEFT_GUI", # extra
    "Gui":"GUI", # extra
    "Windows":"WINDOWS", # extra
    "Command":"COMMAND", # extra
    "Right_Control":"RIGHT_CONTROL", # extra
    "Right_Shift":"RIGHT_SHIFT", # extra
    "Right_Alt":"RIGHT_ALT", # extra
    "Right_Gui":"RIGHT_GUI", # extra
}

MACOS_KEYS = {
    "Meta":"⌃",
    "Ctrl":"⌘",
    "Shift":"⇧",
    "Alt":"⌥",
    "Return":"↵",
    "Enter":"⌤",
    "Up":"↑",
    "Down":"↓",
    "Left":"←",
    "Right":"→",
    "Esc":"⎋",
    "Backspace":"⌫",
    "End":"↘",
    "Home":"↖",
    "Del":"⌦",
    "PgDown":"⇟",
    "PgUp":"⇞",
    "Tab":"⇥",
    "CapsLock":"⇪"

}

MACOS_KEYS_Inverted = {v: k for k, v in MACOS_KEYS.items()}

SHIFT_FIX = {
        "~": "`",
        "!": "1",
        "@": "2",
        "#": "3",
        "$": "4",
        "%": "5",
        "^": "6",
        "&": "7",
        "*": "8",
        "(": "9",
        ")": "0",
        "_": "-",
        "+": "=",
        "{": "[",
        "}": "]",
        ":": ";",
        '"': "'",
        "<": ",",
        ">": ".",
        "?": "/",

        }

DEFAULT_HOTKEYS = [
    ['ONE'],
    ['TWO'],
    ['THREE'],
    ['FOUR'],
    ['FIVE'],
    ['TAB'],
    ['Q'],
    ['W'],
    ['E'],
    ['R'],
    ['CAPS_LOCK'],
    ['A'],
    ['S'],
    ['D'],
    ['F'],
    ['SHIFT'],
    ['Z'],
    ['X'],
    ['C'],
    ['CONTROL'],
    ['OPTION'],
    ['COMMAND'],
    ['SPACE'],
]
class KeySequenceEdit(QtWidgets.QKeySequenceEdit):
    def keyPressEvent(self, event):
        super(KeySequenceEdit, self).keyPressEvent(event)
        seq_string = self.keySequence().toString(QtGui.QKeySequence.PortableText)
        t = self.keySequence().toString(QtGui.QKeySequence.NativeText)
        if seq_string:
            last_seq = seq_string.strip()
            if last_seq in SHIFT_FIX.keys() and len(last_seq) == 1:
                last_seq = "Shift+"+SHIFT_FIX[last_seq]
            _last_seq = last_seq.split("+")
            txt = []
            for key in _last_seq:
                if key in MACOS_KEYS.keys():
                    key = MACOS_KEYS[key]
                txt += [key]
            txt = "+".join(txt)
            le = self.findChild(QtWidgets.QLineEdit, "qt_keysequenceedit_lineedit")
            self.setKeySequence(QtGui.QKeySequence(txt))
            le.setText(txt)
            self.editingFinished.emit()


class HotKeyWidget(QtWidgets.QWidget):
    def __init__(self, callback, btnIndex):
        super(HotKeyWidget, self).__init__()
        self.seqList = []
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self._keysequenceedit = KeySequenceEdit(editingFinished=self.on_editingFinished)
        button = QtWidgets.QPushButton("clear", clicked=self._keysequenceedit.clear)
        okbtn = QtWidgets.QPushButton("ok", clicked=callback)
        okbtn.myData = btnIndex
        close = QtWidgets.QPushButton("cancel", clicked=self.close)
        hlay = QtWidgets.QHBoxLayout(self)
        hlay.addWidget(self._keysequenceedit)
        hlay.addWidget(button)
        hlay.addWidget(okbtn)
        hlay.addWidget(close)

    @QtCore.pyqtSlot()
    def on_editingFinished(self):
        txt = self._keysequenceedit.findChild(QtWidgets.QLineEdit, "qt_keysequenceedit_lineedit").displayText()
        seqList = txt.split("+")
        seqList = [ MACOS_KEYS_Inverted.get(i, i) for i in seqList ]
        seqList = [ QT_CONVERSION.get(i, i) for i in seqList ]
        self.seqList = [ QT_TO_ADAFRUIT.get(i, i) for i in seqList ]

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # self.hotkeyList = [[] for i in range(23)]
        self.hotkeyList = DEFAULT_HOTKEYS
        self.en1 = [["COMMAND","Z"], ["COMMAND","SHIFT","Z"]]
        self.en2 = [["LEFT_BRACKET"], ["RIGHT_BRACKET"]]
        self.en3 = [["LEFT_ARROW"], ["RIGHT_ARROW"]]
        self.en4 = [["DOWN_ARROW"], ["UP_ARROW"]]
        self.en5 = [["COMMAND","-"], ["COMMAND","="]]
        self.en6 = [[], []]
        self.en7 = [[], []]
        super().__init__()

        self.setWindowTitle("Setting KeyMap")

        layout = QtWidgets.QGridLayout()
        self.setFixedSize(QtCore.QSize(900, 600))

        self.btn1 = QtWidgets.QPushButton("key 1")
        self.btn1.myData = 1
        self.btn1.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn1, 0, 0)

        self.btn2 = QtWidgets.QPushButton("key 2")
        self.btn2.myData = 2
        self.btn2.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn2, 0, 1)

        self.btn3 = QtWidgets.QPushButton("key 3")
        self.btn3.myData = 3
        self.btn3.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn3, 0, 2)

        self.btn4 = QtWidgets.QPushButton("key 4")
        self.btn4.myData = 4
        self.btn4.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn4, 0, 3)

        self.btn5 = QtWidgets.QPushButton("key 5")
        self.btn5.myData = 5
        self.btn5.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn5, 0, 4)

        self.btn6 = QtWidgets.QPushButton("key 6")
        self.btn6.myData = 6
        self.btn6.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn6, 1, 0)

        self.btn7 = QtWidgets.QPushButton("key 7")
        self.btn7.myData = 7
        self.btn7.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn7, 1, 1)

        self.btn8 = QtWidgets.QPushButton("key 8")
        self.btn8.myData = 8
        self.btn8.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn8, 1, 2)

        self.btn9 = QtWidgets.QPushButton("key 9")
        self.btn9.myData = 9
        self.btn9.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn9, 1, 3)

        self.btn10 = QtWidgets.QPushButton("key 10")
        self.btn10.myData = 10
        self.btn10.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn10, 1, 4)

        self.btn11 = QtWidgets.QPushButton("key 11")
        self.btn11.myData = 11
        self.btn11.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn11, 2, 0)

        self.btn12 = QtWidgets.QPushButton("key 12")
        self.btn12.myData = 12
        self.btn12.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn12, 2, 1)

        self.btn13 = QtWidgets.QPushButton("key 13")
        self.btn13.myData = 13
        self.btn13.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn13, 2, 2)

        self.btn14 = QtWidgets.QPushButton("key 14")
        self.btn14.myData = 14
        self.btn14.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn14, 2, 3)

        self.btn15 = QtWidgets.QPushButton("key 15")
        self.btn15.myData = 15
        self.btn15.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn15, 2, 4)

        self.btn16 = QtWidgets.QPushButton("key 16")
        self.btn16.myData = 16
        self.btn16.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn16, 3, 0, 1, 2)

        self.btn17 = QtWidgets.QPushButton("key 17")
        self.btn17.myData = 17
        self.btn17.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn17, 3, 2)

        self.btn18 = QtWidgets.QPushButton("key 18")
        self.btn18.myData = 18
        self.btn18.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn18, 3, 3)

        self.btn19 = QtWidgets.QPushButton("key 19")
        self.btn19.myData = 19
        self.btn19.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn19, 3, 4)

        self.btn20 = QtWidgets.QPushButton("key 20")
        self.btn20.myData = 20
        self.btn20.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn20, 4, 0)

        self.btn21 = QtWidgets.QPushButton("key 21")
        self.btn21.myData = 21
        self.btn21.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn21, 4, 1)

        self.btn22 = QtWidgets.QPushButton("key 22")
        self.btn22.myData = 22
        self.btn22.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn22, 4, 2)

        self.btn23 = QtWidgets.QPushButton("key 23")
        self.btn23.myData = 23
        self.btn23.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn23, 4, 3, 1, 2)

        self.btnEn1Left = QtWidgets.QPushButton("en1 left")
        self.btnEn1Left.myData = (1, 0)
        self.btnEn1Left.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn1Left, 5, 3)
        self.btnEn1Right = QtWidgets.QPushButton("en1 right")
        self.btnEn1Right.myData = (1, 1)
        self.btnEn1Right.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn1Right, 5, 4)

        self.btnEn2Left = QtWidgets.QPushButton("en2 left")
        self.btnEn2Left.myData = (2, 0)
        self.btnEn2Left.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn2Left, 6, 3)
        self.btnEn2Right = QtWidgets.QPushButton("en2 right")
        self.btnEn2Right.myData = (2, 1)
        self.btnEn2Right.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn2Right, 6, 4)

        self.btnEn3Left = QtWidgets.QPushButton("en3 left")
        self.btnEn3Left.myData = (3, 0)
        self.btnEn3Left.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn3Left, 7, 3)
        self.btnEn3Right = QtWidgets.QPushButton("en3 right")
        self.btnEn3Right.myData = (3, 1)
        self.btnEn3Right.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn3Right, 7, 4)

        self.btnEn4Left = QtWidgets.QPushButton("en4 left")
        self.btnEn4Left.myData = (4, 0)
        self.btnEn4Left.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn4Left, 8, 3)
        self.btnEn4Right = QtWidgets.QPushButton("en4 right")
        self.btnEn4Right.myData = (4, 1)
        self.btnEn4Right.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn4Right, 8, 4)

        self.btnEn5Left = QtWidgets.QPushButton("en5 left")
        self.btnEn5Left.myData = (5, 0)
        self.btnEn5Left.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn5Left, 9, 3)
        self.btnEn5Right = QtWidgets.QPushButton("en5 right")
        self.btnEn5Right.myData = (5, 1)
        self.btnEn5Right.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn5Right, 9, 4)

        self.btnEn6Left = QtWidgets.QPushButton("en6 left")
        self.btnEn6Left.myData = (6, 0)
        self.btnEn6Left.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn6Left, 10, 3)
        self.btnEn6Right = QtWidgets.QPushButton("en6 right")
        self.btnEn6Right.myData = (6, 1)
        self.btnEn6Right.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn6Right, 10, 4)

        self.btnEn7Left = QtWidgets.QPushButton("en7 left")
        self.btnEn7Left.myData = (7, 0)
        self.btnEn7Left.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn7Left, 11, 3)
        self.btnEn7Right = QtWidgets.QPushButton("en7 right")
        self.btnEn7Right.myData = (7, 1)
        self.btnEn7Right.clicked.connect(self.encoderCallback)
        layout.addWidget(self.btnEn7Right, 11, 4)

        btn = QtWidgets.QPushButton("print")
        btn.clicked.connect(self.printCallback)
        layout.addWidget(btn, 12, 4)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.updateUIMapping()
    
    def updateUIMapping(self):
        for i, hotkey in enumerate(self.hotkeyList):
            
            btnID = i + 1
            name = f"btn{btnID}"
            obj = getattr(self, name)
            obj.setText("+".join(hotkey))

        for i in range(7):
            enID = i + 1
            name = f"en{enID}"
            en = getattr(self, name)

            if en == [[],[]]: continue

            nameLeft = f"btn{name.title()}Left"
            obj = getattr(self, nameLeft)
            obj.setText("+".join(en[0]))

            nameRight = f"btn{name.title()}Right"
            obj = getattr(self, nameRight)
            obj.setText("+".join(en[1]))

    def printCallback(self):
        print()
        encoderDict = {}
        for i in self.__dict__:
            if i.startswith("en"):
                if self.__dict__[i] == [[],[]]: continue
                encoderDict[i] = self.__dict__[i]

        dictionary = {
            "shortcuts": self.hotkeyList,
            "wheels":  encoderDict

        }
        json_object = json.dumps(dictionary, indent = 1)
        print(json_object)
        print()

    def addHotkeyToEncoder(self):
        self.button = self.sender()
        btnIndex, sideIndex = self.button.myData
        self.hotkeyEditor.close()
        self._encObj[sideIndex] = self.hotkeyEditor.seqList
        name = f"btnEn{btnIndex}Left"
        if sideIndex == 1:
            name = f"btnEn{btnIndex}Right"
        obj = getattr(self, name)
        obj.setText( "+".join(self.hotkeyEditor.seqList) )
        print("+".join(self.hotkeyEditor.seqList))

    def addHotkey(self):
        self.button = self.sender()
        name = f"btn{self.button.myData}"
        obj = getattr(self, name)
        self.hotkeyEditor.close()
        self.hotkeyList[self.button.myData-1] = self.hotkeyEditor.seqList
        obj.setText( "+".join(self.hotkeyEditor.seqList) )

    def encoderCallback(self):
        button = self.sender()
        
        if "left" in button.text() and "en" in button.text():
            btnIndex = int(button.text()[2])
            sideIndex = 0
            button.myData = (btnIndex, sideIndex)

        if "right" in button.text() and "en" in button.text():
            btnIndex = int(button.text()[2])
            sideIndex = 1
            button.myData = (btnIndex, sideIndex)

        encName = f"en{button.myData[0]}"
        self._encObj = getattr(self, encName)
        self.hotkeyEditor = HotKeyWidget(self.addHotkeyToEncoder, button.myData)
        self.hotkeyEditor.show()

    def btnCallback(self):
        button = self.sender()
        obj = getattr(button, "myData", None)
        if obj is None:
            btnIndex = int(button.text().strip("key ")) - 1
            button.myData = btnIndex
        self.hotkeyEditor = HotKeyWidget(self.addHotkey, button.myData)
        self.hotkeyEditor.show()

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
