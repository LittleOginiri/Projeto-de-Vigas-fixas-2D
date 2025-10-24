import tkinter as tk
import math
import colorsys
from models.beam import Beam
from models.load import Load
<<<<<<< HEAD
=======
from statics.solver import reactions as solve_reactions
>>>>>>> 80e0cdd (.)

class BeamRenderer:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        # paleta fixa para UDL
        self.udl_colors = ["#1a5", "#05a", "#c70", "#940", "#880"]

<<<<<<< HEAD
    # API pública
=======
    # ============ API pública ============
>>>>>>> 80e0cdd (.)
    def draw_scene(self, L_m, loads):
        c = self.canvas
        c.delete("all")
        w, h = c.winfo_width(), c.winfo_height()
        if w < 10 or h < 10:
            return

        margin_x = 80
        x0, x1 = margin_x, w - margin_x
        y_beam = h // 2
<<<<<<< HEAD
        L = max(1e-6, L_m)
=======
        L = max(1e-6, float(L_m))
>>>>>>> 80e0cdd (.)

        def X(xm: float) -> float:
            return x0 + (x1 - x0) * (xm / L)

<<<<<<< HEAD
        # viga
        c.create_line(x0, y_beam, x1, y_beam, width=4, fill="#444")
        # apoios
        self._support_pin(X(0), y_beam)
        self._support_roller(X(L), y_beam)
        # eixo/grade
        self._axis_ticks(X, y_beam, L)

        # cargas (seta + texto em cima da carga)
        udl_count = 0
        for ld in loads:
            if ld.kind == "POINT":
                self._point_load(X(ld.x), y_beam, ld.magnitude, math.radians(ld.angle_deg), ld.angle_deg)
            else:
                self._udl(X(ld.x1), X(ld.x2), y_beam, ld.magnitude, udl_count)
                udl_count += 1

        # legenda lateral detalhada
        self._legend(w, h, L, loads)
=======
        # --- viga ---
        c.create_line(x0, y_beam, x1, y_beam, width=4, fill="#444")

        # --- apoios ---
        self._support_pin(X(0.0), y_beam)
        self._support_roller(X(L), y_beam)

        # --- eixo/grade ---
        self._axis_ticks(X, y_beam, L)

        # --- cargas (seta + texto em cima da carga) ---
        udl_count = 0
        for ld in loads:
            if ld.kind == "POINT":
                self._point_load(
                    X(ld.x), y_beam,
                    ld.magnitude,
                    math.radians(ld.angle_deg),
                    ld.angle_deg
                )
            else:  # UDL
                self._udl(X(ld.x1), X(ld.x2), y_beam, ld.magnitude, udl_count)
                udl_count += 1

        # --- reações nos apoios (Ax, Ay, Bx, By) ---
        rx = None
        try:
            rx = solve_reactions(L, loads)  # dict: Ax, Ay, Bx(=0), By

            # Escala visual para setas verticais até 80 px
            maxR = max(1.0, abs(rx.get("Ay", 0.0)), abs(rx.get("By", 0.0)))

            def draw_reac_vert(xp: float, val: float, label: str):
                # y positivo é para baixo → para seta "para cima", usamos dy negativo
                dy = -(val / maxR) * 80.0
                self._arrow(xp, y_beam, xp, y_beam + dy, width=3, color="#1e90ff")
                ty = y_beam + dy - 12 if dy < 0 else y_beam + dy + 12
                self.canvas.create_text(
                    xp, ty,
                    text=f"{label} = {val:.2f} N",
                    fill="#1e90ff",
                    font=("Arial", 9),
                    anchor=tk.S if dy < 0 else tk.N
                )

            # Verticais
            draw_reac_vert(X(0.0), rx["Ay"], "Ay")
            draw_reac_vert(X(L),   rx["By"], "By")

            # Horizontal no pino (Ax). Bx = 0 no rolete.
            if abs(rx["Ax"]) > 1e-6:
                dx = (rx["Ax"] / max(abs(rx["Ax"]), 1.0)) * 80.0
                self._arrow(X(0.0), y_beam, X(0.0) + dx, y_beam, width=3, color="#00bcd4")
                ax_label_x = X(0.0) + dx + (8 if dx >= 0 else -8)
                self.canvas.create_text(
                    ax_label_x, y_beam - 12,
                    text=f"Ax = {rx['Ax']:.2f} N",
                    fill="#00bcd4",
                    font=("Arial", 9),
                    anchor=tk.W if dx >= 0 else tk.E
                )
        except Exception:
            # Nunca quebrar a renderização se algo falhar no cálculo
            rx = None

        # --- legenda lateral detalhada (inclui reações) ---
        self._legend(w, h, L, loads, rx)
>>>>>>> 80e0cdd (.)

    # ============ privados ============
    def _axis_ticks(self, X, y_beam, L):
        n_ticks = min(10, max(2, int(L)))
        for i in range(n_ticks + 1):
            xm = L * i / n_ticks
            xp = X(xm)
            self.canvas.create_line(xp, y_beam - 6, xp, y_beam + 6, fill="#888")
            self.canvas.create_text(xp, y_beam + 18, text=f"{xm:.1f}", fill="#666", font=("Arial", 9))

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

    def _point_load(self, x, y_beam, F, theta_rad, angle_deg):
<<<<<<< HEAD
=======
        # Comprimento visível limitado
>>>>>>> 80e0cdd (.)
        max_len = 80
        scale = max_len / (abs(F) + 1e-6)
        L_vis = min(max_len, 20 + abs(F) * scale * 0.25)
        dx = L_vis * math.cos(theta_rad)
        dy = L_vis * math.sin(theta_rad)
        x2, y2 = x + dx, y_beam + dy

        # cor baseada no ângulo (HSV → RGB)
        hue = (angle_deg % 360) / 360.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 0.8)
        color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

        # seta
        self._arrow(x, y_beam, x2, y2, width=2, color=color)

        # texto em cima da seta
        self.canvas.create_text(
            x, y_beam + dy - 12,
            text=f"{F:.0f} N",
            fill=color,
            font=("Arial", 10, "bold")
        )

    def _udl(self, x1, x2, y_beam, w, index):
        c = self.canvas
        color = self.udl_colors[index % len(self.udl_colors)]
        c.create_line(x1, y_beam - 34, x2, y_beam - 34, fill=color)
        n = max(3, int((x2 - x1) / 50))
        for i in range(n):
            t = i / (n - 1) if n > 1 else 0
            x = x1 + t * (x2 - x1)
            self._arrow(x, y_beam - 30, x, y_beam - 4, width=2, color=color)

        # texto no meio da carga distribuída
        c.create_text(
            (x1 + x2) / 2, y_beam - 46,
            text=f"w = {w:.0f} N/m",
            fill=color,
            font=("Arial", 10, "bold")
        )

    def _arrow(self, x1, y1, x2, y2, width=2, color="#000"):
        self.canvas.create_line(x1, y1, x2, y2, width=width, fill=color, arrow=tk.LAST)

<<<<<<< HEAD
    def _legend(self, w, h, L, loads):
        x0, y0 = w - 260, h - 200
        c = self.canvas
        c.create_rectangle(x0, y0, x0 + 250, y0 + 190, outline="#999")
        
        # título
        c.create_text(x0 + 8, y0 + 10, anchor=tk.NW, text="Legenda:", font=("Arial", 10, "bold"))
        
        # comprimento
        c.create_text(x0 + 8, y0 + 30, anchor=tk.NW, text=f"Comprimento L = {L:.2f} m", font=("Arial", 9))
        
=======
    def _legend(self, w, h, L, loads, rx=None):
        x0, y0 = w - 260, h - 200
        c = self.canvas
        c.create_rectangle(x0, y0, x0 + 250, y0 + 190, outline="#999")

        # título
        c.create_text(x0 + 8, y0 + 10, anchor=tk.NW, text="Legenda:", font=("Arial", 10, "bold"))

        # comprimento
        c.create_text(x0 + 8, y0 + 30, anchor=tk.NW, text=f"Comprimento L = {L:.2f} m", font=("Arial", 9))

>>>>>>> 80e0cdd (.)
        # cargas detalhadas
        y_text = y0 + 50
        if not loads:
            c.create_text(x0 + 8, y_text, anchor=tk.NW, text="Nenhuma carga adicionada", font=("Arial", 9, "italic"))
<<<<<<< HEAD
        else:
            for i, ld in enumerate(loads):
                if ld.kind == "POINT":
                    txt = f"[{i}] POINT: {ld.magnitude:.1f} N @ x={ld.x:.2f} m, θ={ld.angle_deg:.1f}°"
                else:
                    txt = f"[{i}] UDL: {ld.magnitude:.1f} N/m de {ld.x1:.2f} m a {ld.x2:.2f} m"
                c.create_text(x0 + 8, y_text, anchor=tk.NW, text=txt, font=("Arial", 9))
                y_text += 16
=======
            y_text += 18
    

        # reações na legenda (opcional)
        if rx is not None:
            y_text += 6
            c.create_text(x0 + 8, y_text, anchor=tk.NW, text="Reações:", font=("Arial", 9, "bold"), fill="#1e90ff")
            y_text += 16
            c.create_text(x0 + 8, y_text, anchor=tk.NW, text=f"Ax = {rx['Ax']:.2f} N", font=("Arial", 9), fill="#00bcd4")
            y_text += 16
            c.create_text(x0 + 8, y_text, anchor=tk.NW, text=f"Ay = {rx['Ay']:.2f} N", font=("Arial", 9), fill="#1e90ff")
            y_text += 16
            c.create_text(x0 + 8, y_text, anchor=tk.NW, text=f"Bx = {rx['Bx']:.2f} N", font=("Arial", 9), fill="#00bcd4")
            y_text += 16
            c.create_text(x0 + 8, y_text, anchor=tk.NW, text=f"By = {rx['By']:.2f} N", font=("Arial", 9), fill="#1e90ff")
>>>>>>> 80e0cdd (.)
