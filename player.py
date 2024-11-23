import turtle
from collision import check_collision
from object import from_shapepoly
from input import Input

class Player(turtle.Turtle):
    def __init__(self, event):
        super().__init__(shape="square", visible=False)
        self.speed("fast")
        self.objects = None
        self.object = from_shapepoly(self.get_shapepoly(), x=0, y=0)
        self.event = event
        self.tick = 50
        self.denominator = 350

        self.x_acceleration = 0
        self.x_velocity = 0
        self.y_acceleration = -9.8
        self.y_velocity = 0

        self.grounded = False

        self.input_up = Input("w")
        self.input_left = Input("a")
        self.input_right = Input("d")

    def set_start(self):
        self.pu()
        for object in self.objects:
            if object.type != "start": continue
            self.goto(object.x, object.y)
            break
        self.pd()

    def check_collisions(self, x, y):
        checked = False
        for object in self.objects:
            if object.type == "start" or object.type == "decor": continue
            self.object.x, self.object.y = x, y
            position = check_collision(object, self.object)
            if position:
                match object.type:
                    case "death":
                        self.event("death")
                        return False, False
                    case "end":
                        self.event("end")
                        return False, False
                    case "bounce":
                        x, y = position
                        if object.y + object.h / 2 <= y - self.object.h / 2:
                            self.y_velocity *= -1
                            self.x_velocity *= 1
                            self.grounded = False
                    case _:
                        x, y = position
                        self.resolve_collision(object, x, y)
                        checked = True
        if not checked: self.grounded = False
        return x, y

    def resolve_collision(self, object, x, y):
        if object.y + object.h / 2 <= y - self.object.h / 2:
            self.grounded = True
            self.y_velocity = 0
        elif object.y - object.h / 2 >= y + self.object.h / 2:
            self.y_velocity = 0
            self.grounded = False
        else:
            if object.x - object.w / 2 <= x + self.object.w / 2:
                self.x_velocity = 0
            elif object.x + object.w / 2 >= x - self.object.w / 2:
                self.x_velocity = 0
            self.grounded = False

    def mainloop(self):
        if self.input_left.down and self.input_right.down:
            self.x_acceleration = 0
        elif self.input_left.down:
            self.x_acceleration = -10
        elif self.input_right.down:
            self.x_acceleration = 10
        else:
            self.x_acceleration = 0
            if self.grounded:
                self.x_velocity *= 0.9

        self.x_velocity += self.x_acceleration * self.tick / self.denominator
        self.y_velocity += self.y_acceleration * self.tick / self.denominator
        x = self.xcor() + self.x_velocity * self.tick / self.denominator
        y = self.ycor() + self.y_velocity * self.tick / self.denominator

        x, y  = self.check_collisions(x, y)
        if not x or not y:
            self.x_acceleration = 0
            self.x_velocity = 0
            self.y_velocity = 0
            return

        if self.input_up.down and self.grounded:
            self.y_velocity = 50
            self.grounded = False
        
        self.goto(x, y)
        turtle.ontimer(self.mainloop, self.tick)

if __name__ == "__main__":
    from main import Main
    Main()