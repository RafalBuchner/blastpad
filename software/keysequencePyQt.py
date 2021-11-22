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


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self._keysequenceedit = KeySequenceEdit(editingFinished=self.on_editingFinished)
        button = QtWidgets.QPushButton("clear", clicked=self._keysequenceedit.clear)
        close = QtWidgets.QPushButton("close", clicked=self.close)
        hlay = QtWidgets.QHBoxLayout(self)
        hlay.addWidget(self._keysequenceedit)
        hlay.addWidget(button)
        hlay.addWidget(close)

    @QtCore.pyqtSlot()
    def on_editingFinished(self):
        txt = self._keysequenceedit.findChild(QtWidgets.QLineEdit, "qt_keysequenceedit_lineedit").displayText()
        seqList = txt.split("+")
        seqList = [ MACOS_KEYS_Inverted.get(i, i) for i in seqList ]
        seqList = [ QT_CONVERSION.get(i, i) for i in seqList ]
        seqList = [ QT_TO_ADAFRUIT.get(i, i) for i in seqList ]
        print(seqList)

if __name__ == '__main__':
    import sys 
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())