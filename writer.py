import turtle

class Writer(turtle.Turtle):
    def __init__(self) -> None:
            super().__init__(visible = False)
            self.pu()
            self.screen = self.getscreen()

    def text(self, text, position=(0, 0), font=("Arial", 16, "normal"), color="black", clear = False):
            self.screen.tracer(0)
            if clear: self.clear()
            self.goto(position)
            self.color(color)
            self.write(text, align="center", font=font)
            self.screen.tracer(1)

if __name__ == "__main__":
    from main import Main
    Main()