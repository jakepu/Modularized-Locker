from pad4pi import rpi_gpio

class KeyPad():
    def log_key(self, key):
        self.output.append(key)
    def __init__(self):
        self.layout = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            ["*", 0, "#"]
        ]

        self.ROW_PINS = [4, 14, 15, 17] # BCM numbering
        self.COL_PINS = [18, 27, 22] # BCM numbering

        factory = rpi_gpio.KeypadFactory()

        self.kp = factory.create_keypad(keypad=self.layout, row_pins=self.ROW_PINS, col_pins=self.COL_PINS)
        # printKey will be called each time a keypad button is pressed
        self.kp.registerKeyPressHandler(log_key)
        self.output = ''
    def reset(self):
        self.output = ''
    

    