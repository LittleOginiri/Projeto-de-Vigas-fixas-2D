# main.py
import tkinter as tk
from tkinter import messagebox
from typing import Optional

from models import Load, BeamModel
from ui import BeamUI
from renderer import BeamRenderer
from validation import validate_point, validate_interval


class BeamApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Viga 2D – Template")
        self.geometry("1100x640")
        self.minsize(1000, 620)

        # Modelo
        self.model = BeamModel()

        # UI (construída no módulo ui.py)
        self.ui = BeamUI(
            self, self.model,
            on_length_change=self._on_length_change,
            on_add_load=self._add_load,
            on_remove_selected=self._remove_selected,
            on_clear_loads=self._clear_loads,
            on_canvas_resize=self.draw
        )

        # Renderizador (desenho no Canvas)
        self.renderer = BeamRenderer(self.ui.canvas)

        # Desenho inicial
        self.draw()

    # ----------------- Manipulação de modelo -----------------
    def _on_length_change(self):
        try:
            L = float(self.ui.len_var.get())
        except ValueError:
            messagebox.showerror("Valor inválido", "Comprimento deve ser numérico.")
            return

        if L <= 0:
            messagebox.showerror("Valor inválido", "O comprimento deve ser positivo.")
            return

        self.model.length_m = L
        self._refresh_list()
        self.draw()

    def _add_load(self):
        kind = self.ui.kind_var.get()
        try:
            if kind == "POINT":
                F = float(self.ui.point_F.get())
                x = float(self.ui.point_x.get())
                theta = float(self.ui.point_theta.get())
                validate_point(self.model, x)
                self.model.loads.append(Load(kind="POINT", magnitude=F, x=x, angle_deg=theta))
            else:
                w = float(self.ui.udl_w.get())
                x1 = float(self.ui.udl_x1.get())
                x2 = float(self.ui.udl_x2.get())
                validate_interval(self.model, x1, x2)
                self.model.loads.append(Load(kind="UDL", magnitude=w, x1=x1, x2=x2))
        except ValueError:
            messagebox.showerror("Entrada inválida", "Verifique os valores numéricos.")
            return
        except AssertionError as e:
            messagebox.showerror("Entrada inválida", str(e))
            return

        self._refresh_list()
        self.draw()

    def _remove_selected(self):
        idx = self._selected_index()
        if idx is None:
            return
        del self.model.loads[idx]
        self._refresh_list()
        self.draw()

    def _clear_loads(self):
        if not self.model.loads:
            return
        if messagebox.askyesno("Confirmar", "Remover todas as cargas?"):
            self.model.loads.clear()
            self._refresh_list()
            self.draw()

    def _selected_index(self) -> Optional[int]:
        sel = self.ui.load_list.curselection()
        if not sel:
            return None
        return int(sel[0])

    def _refresh_list(self):
        self.ui.load_list.delete(0, tk.END)
        for ld in self.model.loads:
            self.ui.load_list.insert(tk.END, ld.label())

    # ---------------------- Desenho ----------------------
    def draw(self):
        self.renderer.draw_scene(self.model.length_m, self.model.loads)


if __name__ == "__main__":
    app = BeamApp()
    app.mainloop()
