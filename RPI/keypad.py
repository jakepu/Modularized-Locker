from pad4pi import rpi_gpio

class KeyPad():
    def log_key(self, key):
        self.output=self.output+str(key)
        print(str(key))
    def __init__(self):
        self.layout = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            ["*", 0, "#"]
        ]

        self.ROW_PINS = [26, 19, 13, 6] # BCM numbering
        self.COL_PINS = [21, 20, 16] # BCM numbering

        factory = rpi_gpio.KeypadFactory()

        self.kp = factory.create_keypad(keypad=self.layout, row_pins=self.ROW_PINS, col_pins=self.COL_PINS)
        # printKey will be called each time a keypad button is pressed
        self.kp.registerKeyPressHandler(self.log_key)
        self.output = ''
    def reset(self):
        self.output = ''
    

    