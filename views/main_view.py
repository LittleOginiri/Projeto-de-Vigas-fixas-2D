import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.beam_controller import BeamController
from app.models.beam import Beam

class MainView(tk.Tk):
    def __init__(self, controller: BeamController | None = None):
        super().__init__()
        self.title("Simulação de Vigas 2D")
        self.controller = controller or BeamController(Beam(length_m=5.0))
        # aqui você move os widgets/frames do seu ui.py original

    # exemplos de handlers
    def on_set_length(self, value: float):
        self.controller.set_length(value)

    def on_add_point(self, mag: float, x: float, ang: float):
        self.controller.add_point_load(mag, x, ang)