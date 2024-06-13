import tkinter as tk
from tkinter import ttk
from utils import OrganismType
from animals.Animal import Animal
from plants.Plant import Plant

import pickle
import os


class SimulationWindow(tk.Frame):
    CELL_SIZE = 30

    def __init__(self, master, simulation, world=None):
        super().__init__(master)
        self.simulation = simulation
        if world:
            self.world = world
        else:
            self.world = simulation.world
        self.create_grid_display()
        self.create_console_log()
        self.create_control_buttons()
        self.draw_grid()
        self.update_console_log()
        self.pack(fill="both", expand=True)
        self.master.bind("<KeyPress>", self.on_key_press)

    def on_key_press(self, event):
        if event.char in ["w", "s", "a", "d", "q"]:
            self.simulation.world.human_input = event.char

    def create_grid_display(self):
        grid_frame = tk.Frame(self)
        grid_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.grid = tk.Canvas(grid_frame, width=self.simulation.world.width * SimulationWindow.CELL_SIZE,
                              height=self.simulation.world.height * SimulationWindow.CELL_SIZE)
        self.grid.pack()
        self.grid.bind("<Button-1>", self.on_grid_click)
        self.draw_grid()

    def on_grid_click(self, event):
        x = event.x // SimulationWindow.CELL_SIZE
        y = event.y // SimulationWindow.CELL_SIZE
        pos = (x, y)

        if self.simulation.world.is_pos_free(pos):
            self.select_organism(pos)

    def select_organism(self, pos):
        popup = tk.Toplevel(self.master)
        popup.title("Select Organism")

        organisms = [
            "Wolf",
            "Sheep",
            "Fox",
            "Turtle",
            "Antilope",
            "Cybersheep",
            "Human",
            "Grass",
            "Sonchus",
            "Guarana",
            "Belladonna",
            "H_Sosnowskyi"
        ]

        listbox = tk.Listbox(popup, width=20, height=len(organisms))
        for organism in organisms:
            listbox.insert(tk.END, organism)
        listbox.pack(padx=10, pady=10)

        # Define a function to create the selected organism
        def create_selected_organism(event):
            selected_index = listbox.curselection()[0]
            selected_organism = organisms[selected_index]
            organism_type = OrganismType[selected_organism.upper()]
            organism_class = self.world.get_organism_by_type(organism_type)
            if issubclass(organism_class, Plant):
                self.simulation.world.create_plant_chunk_at_pos(
                    organism_type, pos)
            elif issubclass(organism_class, Animal):
                self.simulation.world.create_organism_at_pos(
                    organism_type, pos)
            popup.destroy()
            self.simulation.world.update_matrix()
            self.draw_grid()

        # Bind the listbox to the create function
        listbox.bind("<<ListboxSelect>>", create_selected_organism)

    def draw_grid(self):
        organism_colors = {
            OrganismType.WOLF: "brown",
            OrganismType.SHEEP: "lightgray",
            OrganismType.FOX: "orange",
            OrganismType.TURTLE: "green",
            OrganismType.ANTILOPE: "tan",
            OrganismType.CYBERSHEEP: "purple",
            OrganismType.GRASS: "lightgreen",
            OrganismType.SONCHUS: "yellow",
            OrganismType.GUARANA: "red",
            OrganismType.BELLADONNA: "darkred",
            OrganismType.H_SOSNOWSKYI: "darkgreen",
            OrganismType.HUMAN: "blue"
        }
        self.grid.delete("all")
        for row in range(self.simulation.world.height):
            for col in range(self.simulation.world.width):
                x1 = col * SimulationWindow.CELL_SIZE
                y1 = row * SimulationWindow.CELL_SIZE
                x2 = x1 + SimulationWindow.CELL_SIZE
                y2 = y1 + SimulationWindow.CELL_SIZE
                organism_type = self.simulation.world.matrix[row][col]
                if organism_type != " ":
                    organism_color = organism_colors.get(
                        organism_type, "black")
                    organism_symbol = organism_type.name[0].upper()

                    # Check if the organism is an instance of the Animal class
                    organism_class = self.simulation.world.get_organism_by_type(
                        organism_type)
                    if issubclass(organism_class, Animal):
                        self.grid.create_rectangle(
                            x1, y1, x2, y2, fill=organism_color, outline="black", width=4)
                    else:
                        self.grid.create_rectangle(
                            x1, y1, x2, y2, fill=organism_color, outline="black")

                    self.grid.create_text(
                        x1 + SimulationWindow.CELL_SIZE // 2,
                        y1 + SimulationWindow.CELL_SIZE // 2,
                        text=organism_symbol, font=("Arial", 12), fill="white")
                else:
                    self.grid.create_rectangle(
                        x1, y1, x2, y2, fill="white", outline="black")

    def create_console_log(self):
        console_frame = tk.Frame(self)
        console_frame.pack(side=tk.LEFT, padx=10, pady=10,
                           fill=tk.BOTH, expand=True)
        self.console = tk.Text(
            console_frame, wrap=tk.WORD, width=40, height=20)
        self.console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.console_scrollbar = ttk.Scrollbar(
            console_frame, orient=tk.VERTICAL, command=self.console.yview)
        self.console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.configure(yscrollcommand=self.console_scrollbar.set)

    def create_control_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        save_button = tk.Button(button_frame, text="Save",
                                command=self.save_simulation)
        save_button.pack(side=tk.TOP, pady=5)

        load_button = tk.Button(button_frame, text="Load",
                                command=self.load_simulation)
        load_button.pack(side=tk.TOP, pady=5)

        next_turn_button = tk.Button(
            button_frame, text="Next Turn", command=self.next_turn)
        next_turn_button.pack(side=tk.TOP, pady=5)

        exit_button = tk.Button(
            button_frame, text="Exit", command=self.master.destroy)
        exit_button.pack(side=tk.TOP, pady=5)

        self.organism_count_label = tk.Label(button_frame, text="Organisms: 0")
        self.organism_count_label.pack(side=tk.TOP, pady=5)

        self.turn_count_label = tk.Label(button_frame, text=f"Turn: {
                                         self.simulation.world.turn_num}")
        self.turn_count_label.pack(side=tk.TOP, pady=5)

    def update_labels(self):
        self.organism_count_label.configure(
            text=f"Organisms: {len(self.simulation.world.organisms)}")
        self.turn_count_label.configure(
            text=f"Turn: {self.simulation.world.turn_num}")

    def next_turn(self):
        self.simulation.world.make_turn()
        self.update_labels()
        self.draw_grid()
        self.update_console_log()

    def update_console_log(self):
        if self.simulation.world.wlistener.events:
            self.console.insert(
                tk.END, f"\n- Turn {self.simulation.world.turn_num}:\n")
            while self.simulation.world.wlistener.events:
                event = self.simulation.world.wlistener.events.pop()
                self.console.insert(tk.END, event + "\n")

        self.console.yview(tk.END)

    def save_simulation(self):
        file_path = os.path.join(os.getcwd(), "sim.bin")
        with open(file_path, "wb") as file:
            pickle.dump(self.simulation.world, file)

    def load_simulation(self):
        file_path = os.path.join(os.getcwd(), "sim.bin")
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                loaded_world = pickle.load(file)
                self.simulation.world = loaded_world
                self.draw_grid()
                self.update_console_log()
        else:
            print("Simulation file not found.")
