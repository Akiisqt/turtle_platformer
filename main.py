import turtle
from render import Render
from object import load_objects_from_file
from player import Player
from writer import Writer

class Main:
    def __init__(self, level=0):
        self.level = level
        self.screen = turtle.Screen()
        self.screen.listen()

        self.render = Render()
        self.writer = Writer()
        self.player = Player(self.handle_event)

        self.debounce = False

        self.main_menu()
        self.screen.mainloop()
        
    def main_menu(self):
        self.debounce = True
        self.render.clear()
        self.player.clear()
        self.player.ht()
        self.writer.text("Press 'Enter' to Start", position=(0, 375), clear = True)
        self.debounce = False
        self.screen.onkey(self.start_game, "Return")

    def start_game(self):
        if self.debounce:
            return
        self.debounce = True
        print(self.debounce)
        self.writer.clear()

        objects = load_objects_from_file(f"levels/{self.level}.json")
        if not objects:
            self.level = 0
            return self.main_menu()
        
        self.render.clear()
        self.render.update(objects)

        self.player.objects = objects
        self.player.set_start()
        self.player.clear()
        self.player.st()

        self.render_velocity()
        self.player.mainloop()

    def render_velocity(self):
        if self.debounce:
            self.writer.text(
                f"{round(self.player.x_velocity)}, {round(self.player.y_velocity)}",
                position=(0, -388),
                clear=True,
            )
            self.screen.ontimer(self.render_velocity, self.player.tick)

    def handle_event(self, type):
        match type:
            case "death":
                self.debounce = False
                self.writer.clear()
                self.writer.text("You Died!", position=(0, 375),clear=True)
                self.writer.text("Press 'Enter' to Restart", position=(0, 350))
                self.screen.onkey(self.start_game, "Return")
            case "end":
                self.level += 1
                self.debounce = False
                self.start_game()

if __name__ == "__main__":
    Main()
