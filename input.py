import turtle

class Input:
    def __init__(self, key):
        self.key = key
        self.down = False
        self.screen = turtle.Screen()
        self.screen.onkeypress(self.press, self.key)
        self.screen.onkeyrelease(self.release, self.key)

    def press(self):
        self.down = True

    def release(self):
        self.down = False

if __name__ == "__main__":
    from main import Main
    Main()