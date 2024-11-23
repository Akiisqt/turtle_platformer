import turtle

class Render(turtle.Turtle):
    def __init__(self, objects=None) -> None:
        super().__init__(visible=False)
        self.speed(0)
        self.objects = objects or []
        self.screen = self.getscreen()
        self.update(self.objects)

    def update(self, objects=None):
        self.screen.tracer(0)
        objects = objects or self.objects
        self.clear()

        for object in objects:
            if object.type == "start": continue
            self.draw(object)

        self.screen.tracer(1)

    def draw(self, object):
        self.color(object.color)
        self.pu()
        points = object.boundingbox()

        self.goto(points[0])
        self.pd()
        self.begin_fill()

        for point in points[1:]:
            self.goto(point)

        self.goto(points[0])
        self.end_fill()

if __name__ == "__main__":
    from main import Main
    Main()