import sys, os, copy
import json
from collections import OrderedDict
import pprint
from PyQt5 import QtCore, QtGui, QtWidgets

CONFIG_PATH = "/Volumes/BlastPad/configs"

def convertSymbolicToAdafruitNames(shortcut):
    shortcut = [ SYSTEM_KEY_SYMBOLS_Inverted.get(i, i) for i in shortcut ]
    shortcut = [ QT_CONVERSION.get(i, i) for i in shortcut ]
    shortcut = [ QT_TO_ADAFRUIT.get(i, i) for i in shortcut ]
    return shortcut

def convertAdafruitToSymbolicNames(shortcut):
    shortcut = [ QT_TO_ADAFRUIT_Inverted.get(i, i) for i in shortcut ]
    shortcut = [ SYSTEM_KEY_SYMBOLS.get(i, i) for i in shortcut ]
    # shortcut = [ QT_CONVERSION_Inverted.get(i, i) for i in shortcut ]
    return shortcut
    
def convertAdafruitConfigToSymbolic(blastPadDict):
    blastPadDict["shortcuts"] = [convertAdafruitToSymbolicNames(shortcut) for shortcut in blastPadDict["shortcuts"]]
    for enName, shortcuts in blastPadDict["wheels"].items():
        blastPadDict["wheels"][enName] = [convertAdafruitToSymbolicNames(shortcut) for shortcut in shortcuts]
    return blastPadDict

if sys.platform == "darwin":
    QT_CONVERSION = {
            "Meta":"Control",
            "Ctrl":"Command",
            "Alt":"Option",
            "Esc":"Escape",
            "Del":"Delete",
        }
else:
    QT_CONVERSION = {
            "Meta":"Windows",
            "Ctrl":"Control",
            "Esc":"Escape",
            "Del":"Delete",
        }

QT_CONVERSION_Inverted = {v: k for k, v in QT_CONVERSION.items()}


SYSTEM_KEY_SYMBOLS = {
    "Meta":"⌃",
    "Ctrl":"⌘",
    "Command":"⌘",
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

SYSTEM_KEY_SYMBOLS_Inverted = {v: k for k, v in SYSTEM_KEY_SYMBOLS.items()}

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

QT_TO_ADAFRUIT_Inverted = {v: k for k, v in QT_TO_ADAFRUIT.items()}


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

DEFAULT_HOTKEYS = [ convertAdafruitToSymbolicNames(shortcut) for shortcut in  [['ONE'], ['TWO'], ['THREE'], ['FOUR'], ['FIVE'], ['TAB'], ['Q'], ['W'], ['E'], ['R'], ['CAPS_LOCK'], ['A'], ['S'], ['D'], ['F'], ['SHIFT'], ['Z'], ['X'], ['C'], ['CONTROL'], ['OPTION'], ['COMMAND'], ['SPACE']]]
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
                if key in SYSTEM_KEY_SYMBOLS.keys():
                    key = SYSTEM_KEY_SYMBOLS[key]
                txt += [key]
            txt = "+".join(txt)
            le = self.findChild(QtWidgets.QLineEdit, "qt_keysequenceedit_lineedit")
            self.setKeySequence(QtGui.QKeySequence(txt))
            le.setText(txt)
            self.editingFinished.emit()


class HotKeyWidget(QtWidgets.QWidget):
    do_convert_to_adafruit_names = False
    def __init__(self, callback, myData):
        super(HotKeyWidget, self).__init__()
        self.shortcut = []
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self._keysequenceedit = KeySequenceEdit(editingFinished=self.on_editingFinished)
        button = QtWidgets.QPushButton("clear", clicked=self._keysequenceedit.clear)
        okbtn = QtWidgets.QPushButton("ok", clicked=callback)
        okbtn.myData = myData
        close = QtWidgets.QPushButton("cancel", clicked=self.close)
        hlay = QtWidgets.QHBoxLayout(self)
        hlay.addWidget(self._keysequenceedit)
        hlay.addWidget(button)
        hlay.addWidget(okbtn)
        hlay.addWidget(close)

    @QtCore.pyqtSlot()
    def on_editingFinished(self):
        txt = self._keysequenceedit.findChild(QtWidgets.QLineEdit, "qt_keysequenceedit_lineedit").displayText()
        shortcut = txt.split("+")
        
        if self.do_convert_to_adafruit_names:
            shortcut = convertSymbolicToAdafruitNames(shortcut)
        self.shortcut = shortcut





class TextWidget(QtWidgets.QWidget):
    def __init__(self, callback, myData):
        super(TextWidget, self).__init__()
        self.shortcut = []
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self._textedit = QtWidgets.QLineEdit()
        button = QtWidgets.QPushButton("clear", clicked=self._textedit.clear)
        okbtn = QtWidgets.QPushButton("ok", clicked=callback)
        okbtn.myData = myData
        close = QtWidgets.QPushButton("cancel", clicked=self.close)
        hlay = QtWidgets.QHBoxLayout(self)
        hlay.addWidget(self._textedit)
        hlay.addWidget(button)
        hlay.addWidget(okbtn)
        hlay.addWidget(close)
    
    def getText(self):
        return self._textedit.displayText()
# data = OrderedDict((
#         ('name',['1','2','3','4','1']),
#         ('hotkey 1',[]),
#         ('hotkey 2',[])
#         ))

encoderData = [
        {'Undo/Redo':[convertAdafruitToSymbolicNames(shortcut) for shortcut in [ ['Command', 'Z'], ['Shift', 'Command', 'Z'] ]]},
        ]

class QHLine(QtWidgets.QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

class EncoderTable(QtWidgets.QTableWidget):
    def __init__(self, data, *args):
        QtWidgets.QTableWidget.__init__(self, *args)
        self._encData = data
        self.setData()  
        self.verticalHeader().setVisible(False)
        self.setEditTriggers( QtWidgets.QAbstractItemView.NoEditTriggers )
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.cellDoubleClicked.connect(self.cellDoubleClickedCallback)
        self.selectRow(0)

    def importData(self, data):
        self._encData = []
        for k, i in data.items():
            self._encData.append( {k:i})
        self.setData()

    @property
    def currentEncoderIndex(self):
        return self.currentRow()

    def getLongestHotkeySetLenght(self):
        list_len = [len(list(v.values())[0]) for v in self._encData]
        return max(list_len) 

    def updateColumnCount(self):
        if self.columnCount() <= self.getLongestHotkeySetLenght()+1:
            self.setColumnCount(self.getLongestHotkeySetLenght()+1)
            header = f"hotkey {self.getLongestHotkeySetLenght()}"
            headerItem = QtWidgets.QTableWidgetItem(header)
            self.setHorizontalHeaderItem(self.getLongestHotkeySetLenght(), headerItem)

    @property
    def currentShortcutIndex(self):
        value = self.currentColumn()-1
        if value < 0:
            return
        return self.currentColumn()-1
    
    def setData(self): 
        self.clear()
        self.setColumnCount(self.getLongestHotkeySetLenght()+1)
        self.setRowCount(len(self._encData))

        for row, item in  enumerate(self._encData):
            shortcuts = tuple(item.values())[0]
            nameItem = QtWidgets.QTableWidgetItem(tuple(item.keys())[0])
            self.setItem(row, 0, nameItem)

            for col in range(self.getLongestHotkeySetLenght()):
                if col == len(shortcuts): break
                shortcut = "+".join(shortcuts[col])
                newitem = QtWidgets.QTableWidgetItem(shortcut)
                self.setItem(row, col+1, newitem)

        horHeaders = []
        for i in range(self.getLongestHotkeySetLenght()+1):
            if i == 0:
                header = "name"
            else:
                header = f"hotkey {i}"
            horHeaders.append(header)
        self.setHorizontalHeaderLabels(horHeaders) 

    def __addTableRow(self, row_data):
        row = self.rowCount()
        self.setRowCount(row+1)
        col = 0
        for item in row_data:
            cell = QtWidgets.QTableWidgetItem(str(item))
            self.setItem(row, col, cell)
            col += 1

    def cellDoubleClickedCallback(self, row, col):
        item = self.item(row,col)
        if item is None:
            item = QtWidgets.QTableWidgetItem("New Item")
            _col = col
            if col > len(self.getEncoderShortcuts(row)):
                _col = len(self.getEncoderShortcuts(row))+1
            self.setItem(row, _col, item)
        if col != 0:
            self.hotkeyEditor = HotKeyWidget(self.editHotkeyCallback, (row, col, item))
            self.hotkeyEditor.show()
        else:
            self.textEditor = TextWidget(self.editNameCallback, row)
            self.textEditor.show()

    def _addRow(self):
        self.rowCount()
        self.setRowCount(self.rowCount()+1)

    def _addColumn(self):
        self.columnCount()
        self.setColumnCount(self.columnCount()+1)

    def addEncoder(self, encName, encList):
        self._encData += [{encName:encList}]
        if self.columnCount() < len(encList):
            self.setColumnCount(len(encList) + 1)
        row_data = [encName] + encList
        self.__addTableRow(row_data)



    def getEncoderName(self, encoderIndex):
        return list(self._encData[encoderIndex].keys())[0]

    def getEncoderShortcuts(self, encoderIndex):
        return list(self._encData[encoderIndex].values())[0]

    def deleteEncoders(self, indexes):
        # delete
        self.setData()

    def renameEncoder(self, encoderIndex, newName):
        oldName = self.getEncoderName(encoderIndex)
        oldEncData = copy.deepcopy(self._encData[encoderIndex][oldName])
        self._encData[encoderIndex][newName] = oldEncData
        del self._encData[encoderIndex][oldName]
        item = self.item(encoderIndex, 0)
        item.setText(newName)

    def addHotkeyUI(self):
        if self.currentRow() == -1: return
        self.hotkeyEditor = HotKeyWidget(self.addHotkeyUICallback, None)
        self.hotkeyEditor.show()
        

    def editNameCallback(self):
        encoderIndex = self.sender().myData
        self.textEditor.close()
        newName = self.textEditor.getText()
        self.renameEncoder(encoderIndex, newName)

    def addHotkeyUICallback(self):
        self.hotkeyEditor.close()
        self.__lastHotkey = self.hotkeyEditor.shortcut
        self.addHotkey(self.__lastHotkey, self.currentRow())

    def addHotkey(self, shortcut, encoderIndex):
        # adds column if needed
        # or edits empty cell
        self.getEncoderShortcuts(encoderIndex).append(shortcut)
        self.updateColumnCount()
        col = len(self.getEncoderShortcuts(encoderIndex))
        
        item = QtWidgets.QTableWidgetItem("+".join(shortcut))
        self.setItem(encoderIndex, col, item)   
        
    def getShortcut(self, encoderIndex, shortcutIndex):
        shortcut = self.getEncoderShortcuts(encoderIndex)[shortcutIndex]
        item = self.itemAt(encoderIndex, shortcutIndex+1)
        return dict(shortcut=shortcut, qtItem=item)

    def getShortcutFromTable(self, row, col):
        encoderIndex = row
        shortcutIndex = col + 1
        shortcut = self.getEncoderShortcuts(encoderIndex)[0][shortcutIndex]
        item = self.itemAt(row, col)
        return dict(shortcut=shortcut, qtItem=item)

    def editHotkeyCallback(self):
        row, col, item = self.sender().myData
        encoderIndex = row
        shortcutIndex = col + 1
        self.hotkeyEditor.close()
        self.__lastHotkey = self.hotkeyEditor.shortcut
        
        
        if shortcutIndex >= len(self.getEncoderShortcuts(encoderIndex)):
            self.getEncoderShortcuts(encoderIndex).append(self.__lastHotkey)
        else:
            
            self.getEncoderShortcuts(encoderIndex)[shortcutIndex] = self.__lastHotkey

        item.setText( "+".join(self.__lastHotkey) )
    
    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace]:
            encoderIndex = self.currentRow()
            self.removeEncoder(encoderIndex)
        else:
            super().keyPressEvent(event)

    def removeEncoder(self, encoderIndex):
        ### TODO
        #remove selected Row
        self.removeRow(encoderIndex)
        del self._encData[encoderIndex]
        pass  

    def getFinalData(self):
        data = {}
        for encoderIndex in range(self.rowCount()):
            name = self.getEncoderName(encoderIndex)
            shortcuts = self.getEncoderShortcuts(encoderIndex)
            data[name] = [convertSymbolicToAdafruitNames(shortcut) for shortcut in shortcuts if len(shortcut) != 0]

        return data




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.hotkeyList = DEFAULT_HOTKEYS

        self.setWindowTitle("BlastPad")

        layout = QtWidgets.QGridLayout()
        self.setFixedSize(QtCore.QSize(1000, 700))

        # self.setsCombo = QtWidgets.QComboBox()
        # self.setsCombo.addItems(["default"])
        # layout.addWidget(self.setsCombo, 0, 0)

        # self.addSetBtn = QtWidgets.QPushButton("add set")
        # self.addSetBtn.clicked.connect(self.addSetCallback)
        # layout.addWidget(self.addSetBtn, 0, 1)

        # self.removeSetBtn = QtWidgets.QPushButton("remove set")
        # self.removeSetBtn.clicked.connect(self.removeSetCallback)
        # layout.addWidget(self.removeSetBtn, 0, 2)

        layout.addWidget(QHLine(), 1, 0,1,5)
        
        ###############################################################

        self.btn1 = QtWidgets.QPushButton("key 1")
        self.btn1.myData = 1
        self.btn1.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn1, 2, 0)

        self.btn2 = QtWidgets.QPushButton("key 2")
        self.btn2.myData = 2
        self.btn2.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn2, 2, 1)

        self.btn3 = QtWidgets.QPushButton("key 3")
        self.btn3.myData = 3
        self.btn3.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn3, 2, 2)

        self.btn4 = QtWidgets.QPushButton("key 4")
        self.btn4.myData = 4
        self.btn4.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn4, 2, 3)

        self.btn5 = QtWidgets.QPushButton("key 5")
        self.btn5.myData = 5
        self.btn5.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn5, 2, 4)

        self.btn6 = QtWidgets.QPushButton("key 6")
        self.btn6.myData = 6
        self.btn6.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn6, 3, 0)

        self.btn7 = QtWidgets.QPushButton("key 7")
        self.btn7.myData = 7
        self.btn7.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn7, 3, 1)

        self.btn8 = QtWidgets.QPushButton("key 8")
        self.btn8.myData = 8
        self.btn8.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn8, 3, 2)

        self.btn9 = QtWidgets.QPushButton("key 9")
        self.btn9.myData = 9
        self.btn9.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn9, 3, 3)

        self.btn10 = QtWidgets.QPushButton("key 10")
        self.btn10.myData = 10
        self.btn10.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn10,3, 4)

        self.btn11 = QtWidgets.QPushButton("key 11")
        self.btn11.myData = 11
        self.btn11.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn11, 4, 0)

        self.btn12 = QtWidgets.QPushButton("key 12")
        self.btn12.myData = 12
        self.btn12.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn12, 4, 1)

        self.btn13 = QtWidgets.QPushButton("key 13")
        self.btn13.myData = 13
        self.btn13.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn13, 4, 2)

        self.btn14 = QtWidgets.QPushButton("key 14")
        self.btn14.myData = 14
        self.btn14.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn14, 4, 3)

        self.btn15 = QtWidgets.QPushButton("key 15")
        self.btn15.myData = 15
        self.btn15.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn15, 4, 4)

        self.btn16 = QtWidgets.QPushButton("key 16")
        self.btn16.myData = 16
        self.btn16.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn16, 5, 0, 1, 2)

        self.btn17 = QtWidgets.QPushButton("key 17")
        self.btn17.myData = 17
        self.btn17.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn17, 5, 2)

        self.btn18 = QtWidgets.QPushButton("key 18")
        self.btn18.myData = 18
        self.btn18.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn18, 5, 3)

        self.btn19 = QtWidgets.QPushButton("key 19")
        self.btn19.myData = 19
        self.btn19.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn19, 5, 4)

        self.btn20 = QtWidgets.QPushButton("key 20")
        self.btn20.myData = 20
        self.btn20.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn20, 6, 0)

        self.btn21 = QtWidgets.QPushButton("key 21")
        self.btn21.myData = 21
        self.btn21.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn21, 6, 1)

        self.btn22 = QtWidgets.QPushButton("key 22")
        self.btn22.myData = 22
        self.btn22.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn22, 6, 2)

        self.btn23 = QtWidgets.QPushButton("key 23")
        self.btn23.myData = 23
        self.btn23.clicked.connect(self.btnCallback)
        layout.addWidget(self.btn23, 6, 3, 1, 2)

        layout.addWidget(QHLine(), 7, 0,1,5)
        
        ###############################################################

        self.encTable = EncoderTable(encoderData, 4, 3)
        layout.addWidget(self.encTable, 8, 0, 6, 5)

        btn = QtWidgets.QPushButton("add encoder")
        btn.clicked.connect(self.addEncoderCallback)
        layout.addWidget(btn, 14, 4)

        btn = QtWidgets.QPushButton("add hotkey")
        btn.clicked.connect(self.addHotkeyCallback)
        layout.addWidget(btn, 14, 3)


        btn = QtWidgets.QPushButton("load")
        btn.clicked.connect(self.loadCallback)
        layout.addWidget(btn, 15, 3)

        btn = QtWidgets.QPushButton("save")
        btn.clicked.connect(self.saveCallback)
        layout.addWidget(btn, 15, 4)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.refreshButtons()
    
    def refreshButtons(self):
        for i, hotkey in enumerate(self.hotkeyList):
            btnID = i + 1
            name = f"btn{btnID}"
            obj = getattr(self, name)
            obj.setText("+".join(hotkey))

    def addEncoderCallback(self):
        self.encTable.addEncoder("new encoder", [])
    
    def addHotkeyCallback(self):
        
        self.encTable.addHotkeyUI()

    def getFinalBtnMatrixData(self):
        return [convertSymbolicToAdafruitNames(shortcut) for shortcut in self.hotkeyList]

    def loadCallback(self):
        path = ""
        if os.path.exists(CONFIG_PATH):
            path = CONFIG_PATH
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", path,"json blastpad file (*.json)")
        if fileName == "": return
        with open(fileName, "r") as f:
            blastPadDict = convertAdafruitConfigToSymbolic(json.load(f))

            self.hotkeyList = blastPadDict['shortcuts']
            self.refreshButtons()
            self.encTable.importData(blastPadDict['wheels'])
        pass

    def saveCallback(self):
        json_text = self.getJsonStr()
        path = ""
        if os.path.exists(CONFIG_PATH):
            path = CONFIG_PATH
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()",path,"json blastpad file (*.json)")
        if fileName == "": return
        with open(fileName, "w") as f:
            f.write(json_text)
        print()
        print(json_text)
        print()
    
    def getJsonStr(self):
        encoderDict = self.encTable.getFinalData()
        hotkeyList = self.getFinalBtnMatrixData()

        dictionary = {
            "shortcuts": hotkeyList,
            "wheels":  encoderDict

        }

        json_object = json.dumps(dictionary, indent=1)

        return json_object

    def addHotkey(self):
        self.button = self.sender()
        name = f"btn{self.button.myData}"
        obj = getattr(self, name)
        self.hotkeyEditor.close()
        self.hotkeyList[self.button.myData-1] = self.hotkeyEditor.shortcut
        obj.setText( "+".join(self.hotkeyEditor.shortcut) )

    def addSetCallback(self):
        self.textEditor = TextWidget(self.textEditorCallback, None)
        self.textEditor.show()

    def addSetTextEditorCallback(self):
        ###TODO
        name = self.textEditor.getText()
        self.textEditor.close()

    def removeSetCallback(self):
        ###TODO
        pass

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
