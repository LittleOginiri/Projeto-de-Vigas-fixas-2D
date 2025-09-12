import tkinter as tk
import math
from models.beam import Beam
from models.load import Load

class BeamRenderer:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas

    # API pública
    def draw_scene(self, L_m, loads):
        c = self.canvas
        c.delete("all")
        w, h = c.winfo_width(), c.winfo_height()
        if w < 10 or h < 10:
            return

        margin_x = 80
        x0, x1 = margin_x, w - margin_x
        y_beam = h // 2
        L = max(1e-6, L_m)

        def X(xm: float) -> float:
            return x0 + (x1 - x0) * (xm / L)

        # viga
        c.create_line(x0, y_beam, x1, y_beam, width=4, fill="#444")
        # apoios
        self._support_pin(X(0), y_beam)
        self._support_roller(X(L), y_beam)
        # eixo/grade
        self._axis_ticks(X, y_beam, L)

        # cargas
        for ld in loads:
            if ld.kind == "POINT":
                self._point_load(X(ld.x), y_beam, ld.magnitude, math.radians(ld.angle_deg))
            else:
                self._udl(X(ld.x1), X(ld.x2), y_beam, ld.magnitude)

        # legenda
        self._legend(w, h)

    # ============ privados ============
    def _axis_ticks(self, X, y_beam, L):
        n_ticks = min(10, max(2, int(L)))
        for i in range(n_ticks + 1):
            xm = L * i / n_ticks
            xp = X(xm)
            self.canvas.create_line(xp, y_beam - 6, xp, y_beam + 6, fill="#888")
            self.canvas.create_text(xp, y_beam + 18, text=f"{xm:.1f}", fill="#666", font=("Arial", 9))
        self.canvas.create_text((X(0)+X(L))/2, y_beam - 18, text=f"L = {L:.2f} m", fill="#222", font=("Arial", 10, "bold"))

    def _support_pin(self, x, y):
        size = 18
        c = self.canvas
        c.create_polygon(x - size, y + size, x + size, y + size, x, y, fill="#666", outline="#333")
        c.create_line(x - size - 8, y + size, x + size + 8, y + size, fill="#333")

    def _support_roller(self, x, y):
        size = 18
        c = self.canvas
        c.create_polygon(x - size, y + size, x + size, y + size, x, y, fill="#666", outline="#333")
        r = 5
        for i in (-10, 0, 10):
            c.create_oval(x + i - r, y + size, x + i + r, y + size + 2*r, outline="#333")
        c.create_line(x - size - 8, y + size + 2*r, x + size + 8, y + size + 2*r, fill="#333")

    def _point_load(self, x, y_beam, F, theta_rad):
        max_len = 80
        scale = max_len / (abs(F) + 1e-6)
        L_vis = min(max_len, 20 + abs(F) * scale * 0.25)
        dx = L_vis * math.cos(theta_rad)
        dy = L_vis * math.sin(theta_rad)
        x2, y2 = x + dx, y_beam + dy
        self._arrow(x, y_beam, x2, y2, width=2, color="#d22")
        self.canvas.create_text(x, y_beam + dy - 12, text=f"{F:.0f} N", fill="#b11", font=("Arial", 10, "bold"))

    def _udl(self, x1, x2, y_beam, w):
        c = self.canvas
        c.create_line(x1, y_beam - 34, x2, y_beam - 34, fill="#1a5")
        n = max(3, int((x2 - x1) / 50))
        for i in range(n):
            t = i / (n - 1) if n > 1 else 0
            x = x1 + t * (x2 - x1)
            self._arrow(x, y_beam - 30, x, y_beam - 4, width=2, color="#1a5")
        c.create_text((x1 + x2) / 2, y_beam - 46, text=f"w = {w:.0f} N/m", fill="#0a4", font=("Arial", 10, "bold"))

    def _arrow(self, x1, y1, x2, y2, width=2, color="#000"):
        self.canvas.create_line(x1, y1, x2, y2, width=width, fill=color, arrow=tk.LAST)

    def _legend(self, w, h):
        x0, y0 = w - 260, h - 120
        c = self.canvas
        c.create_rectangle(x0, y0, x0 + 250, y0 + 110, outline="#999")
        c.create_text(x0 + 8, y0 + 10, anchor=tk.NW, text="Legenda:", font=("Arial", 10, "bold"))
        c.create_text(x0 + 8, y0 + 32, anchor=tk.NW, text="• Linha cinza: viga biapoiada (visual)")
        c.create_text(x0 + 8, y0 + 52, anchor=tk.NW, text="• Triângulos: apoios simples em x=0 e x=L")
        c.create_text(x0 + 8, y0 + 72, anchor=tk.NW, text="• Setas vermelhas: cargas concentradas")
        c.create_text(x0 + 8, y0 + 92, anchor=tk.NW, text="• Linha/Setas verdes: carga distribuída (UDL)")