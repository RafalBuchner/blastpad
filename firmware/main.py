from macropad import MacroPadUI
from minikbd import MiniKbdButtons
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
# print(Keycode.__dict__)
kbd = Keyboard(usb_hid.devices)
kbdLayout = KeyboardLayoutUS(kbd)


ui = MacroPadUI()

# def buttonDownCallback(buttonID, othersDown):
#     kbd.press(Keycode.UP_ARROW)
#     print("btn _down_", buttonID, othersDown)

# def buttonUpCallback(buttonID):
#     kbd.release(Keycode.UP_ARROW)
#     print("btn ^UPUP^", buttonID)


# ButtonMatrix = MiniKbdButtons(
#         keyDownCallback=buttonDownCallback, 
#         keyUpCallback=buttonUpCallback
#     )

while True:
    
    ui.update()
    
    # testEn.update()
    