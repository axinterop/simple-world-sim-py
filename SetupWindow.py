import tkinter as tk
import pickle
import os


class SetupWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Simulation Setup")
        self.width = None
        self.world = None
        self.height = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()

    def create_widgets(self):
        width_label = tk.Label(self, text="Width:")
        width_label.grid(row=0, column=0, padx=10, pady=10)

        self.width_entry = tk.Entry(self)
        self.width_entry.grid(row=0, column=1, padx=10, pady=10)

        height_label = tk.Label(self, text="Height:")
        height_label.grid(row=1, column=0, padx=10, pady=10)

        self.height_entry = tk.Entry(self)
        self.height_entry.grid(row=1, column=1, padx=10, pady=10)

        submit_button = tk.Button(self, text="Submit", command=self.submit)
        submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        load_button = tk.Button(
            self, text="Load", command=self.load_simulation)
        load_button.grid(row=2, column=0, padx=5, pady=5)

    def submit(self):
        try:
            self.width = int(self.width_entry.get())
            self.height = int(self.height_entry.get())
            self.destroy()
        except ValueError:
            print("Invalid width or height. Please enter integers.")

    def load_simulation(self):
        file_path = os.path.join(os.getcwd(), "sim.bin")
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                loaded_world = pickle.load(file)
                self.world = loaded_world
                self.destroy()
        else:
            print("Simulation file not found.")

    def on_close(self):
        self.width = None
        self.height = None
        self.destroy()
