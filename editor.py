import turtle
from object import *
from render import *
from writer import Writer
import json

class Editor(turtle.Turtle):
    def __init__(self):
        super().__init__(visible=False)

        self.screen = turtle.Screen()
        self.screen.onclick(self.leftmouse, btn=1)
        self.screen.onclick(self.rightmouse, btn=3)
        self.screen.onkeypress(self.save, "s")
        self.screen.onkeypress(self.delete, "x")
        self.screen.onkeypress(self.change_color, "c")
        self.screen.onkeypress(self.layer_up, ".")
        self.screen.onkeypress(self.layer_down, ",")
        self.screen.onkeypress(self.up, "Up")
        self.screen.onkeypress(self.down, "Down")
        self.screen.onkeypress(self.left, "Left")
        self.screen.onkeypress(self.right, "Right")
        self.screen.onkeypress(self.toggle_size, "m")
        self.screen.onkeypress(self.type, "t")
        self.screen.listen()

        self.objects = load_objects_from_file("levels/data.json")
        self.colors = ["black", "gray", "red", "green", "yellow", "blue", "purple", "white"]
        self.types = ["death", "start", "end", "decor", "bounce", "normal"]
        self.partial = None
        self.selected_obj = None
        self.changing_size = False

        self.render = Render(self.objects)
        self.writer = Writer()
        self.screen.mainloop()

    def leftmouse(self, x, y):
        x, y = round(x), round(y)

        if not self.partial:
            self.partial = [x, y]
        else:
            x1, y1 = self.partial
            w, h = abs(x - x1), abs(y - y1)
            center_x, center_y = (x + x1) / 2, (y + y1) / 2

            self.objects.append(Object(w, h, x=center_x, y=center_y))
            self.partial = None
            self.render.draw(self.objects[-1:][0])
            self.selected_obj = self.objects[-1:][0]

    def rightmouse(self, x, y):
        for object in self.objects:
            if (object.x - object.w / 2 <= x <= object.x + object.w / 2 and object.y - object.h / 2 <= y <= object.y + object.h / 2):
                self.selected_obj = object
                break
    def toggle_size(self):
        self.changing_size = not self.changing_size
    def up(self):
        if not self.selected_obj: return
        if self.changing_size:
            self.selected_obj.h += .5
        else:
            self.selected_obj.y += .5
        self.render.update(self.objects)
    def down(self):
        if not self.selected_obj: return
        if self.changing_size:
            self.selected_obj.h -= .5
        else:
            self.selected_obj.y -= .5
        self.render.update(self.objects)
    def left(self):
        if not self.selected_obj: return
        if self.changing_size:
            self.selected_obj.w -= .5
        else:
            self.selected_obj.x -= .5
        self.render.update(self.objects)
    def right(self):
        if not self.selected_obj: return
        if self.changing_size:
            self.selected_obj.w += .5
        else:
            self.selected_obj.x += .5
        self.render.update(self.objects)
    def delete(self):
        if not self.selected_obj: return
        self.objects.pop(self.objects.index(self.selected_obj))
        self.selected_obj = None
        self.render.update(self.objects)
    def type(self):
        if not self.selected_obj: return
        self.selected_obj.type = self.types[(self.types.index(self.selected_obj.type) + 1) % len(self.types)]
        self.writer.text(self.selected_obj.type, (0, 375), clear = True)
        turtle.ontimer(Writer.clear, 100)
    def change_color(self):
        if not self.selected_obj: return
        self.selected_obj.color = self.colors[(self.colors.index(self.selected_obj.color) + 1) % len(self.colors)]
        self.render.update(self.objects)
    def layer_up(self):
        if not self.selected_obj: return
        index = self.objects.index(self.selected_obj)
        self.objects.pop(index)
        self.objects.insert(index + 1, self.selected_obj)
        self.render.update(self.objects)
    def layer_down(self):
        if not self.selected_obj: return
        index = self.objects.index(self.selected_obj)
        if index <= 0: return
        self.objects.pop(index)
        self.objects.insert(index - 1, self.selected_obj)
        self.render.update(self.objects)
    def save(self):
        with open("levels/data.json", "w") as file:
            json.dump(
                [
                    {
                        "w": object.w,
                        "h": object.h,
                        "x": object.x,
                        "y": object.y,
                        "c": object.color,
                        "t": object.type,
                    }
                    for object in self.objects
                ],
                file,
                separators=(",", ":"),
            )

Editor()