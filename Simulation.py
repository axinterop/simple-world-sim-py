from World import World
from SimulationWindow import SimulationWindow
from SetupWindow import SetupWindow
import tkinter as tk


class Simulation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.world = None
        self.setup_window = SetupWindow(self.root)
        self.setup_window.wait_window(self.setup_window)
        self.create_world()

        if self.world is not None:
            self.window = SimulationWindow(self.root, self, self.world)
            self.root.deiconify()
            self.run()
        else:
            self.root.destroy()

    def create_world(self):
        if self.setup_window.world is not None:
            self.world = self.setup_window.world
        elif self.setup_window.width is not None and self.setup_window.height is not None:
            self.world = World(self.setup_window.width,
                               self.setup_window.height)

    def run(self):
        if hasattr(self, 'window'):
            self.window.mainloop()
