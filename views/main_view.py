import tkinter as tk
from tkinter import ttk, messagebox
from controllers.beam_controller import BeamController
from .render_adapter import RenderAdapter


class MainView(tk.Tk):
    def __init__(self, controller: BeamController | None = None):
        super().__init__()
        self.title("Simulação de Vigas 2D")
        self.geometry("900x600")

        self.controller = controller or BeamController()
        self.adapter = RenderAdapter()

        self._sidebar_collapsed = False
        self._saved_sash = 260  # posição lembrada ao colapsar

        self._build_layout()
        self._render()

    def _build_layout(self):
        # Topbar
        top = ttk.Frame(self, padding=8)
        top.pack(side="top", fill="x")

        ttk.Label(top, text="Comprimento (m):").pack(side="left")
        self.len_var = tk.StringVar(value=str(self.controller.beam.length_m))
        ttk.Entry(top, width=8, textvariable=self.len_var).pack(side="left", padx=(4, 10))
        ttk.Button(top, text="Aplicar", command=self._on_set_length).pack(side="left")

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=6)

        # Paned Window (divisor arrastável)
        self.pw = ttk.Panedwindow(self, orient="horizontal")
        self.pw.pack(side="top", fill="both", expand=True)

        left = ttk.Frame(self.pw, padding=6)   # sidebar
        right = ttk.Frame(self.pw)             # canvas area

        # adiciona painéis com pesos (canvas cresce mais)
        self.pw.add(left, weight=0)
        self.pw.add(right, weight=1)

        # limites mínimos dinâmicos
        self.pw.bind("<Configure>", self._enforce_min_sizes)

        # ============ Conteúdo da sidebar ============ #
        # Carga Pontual
        ttk.Label(left, text="Carga Pontual (N @ x m)").pack(anchor="w")
        pl_frame = ttk.Frame(left)
        pl_frame.pack(fill="x", pady=2)
        self.pl_mag = tk.StringVar(value="1000")
        self.pl_x = tk.StringVar(value="2.0")
        self.pl_ang = tk.StringVar(value="90")
        ttk.Entry(pl_frame, width=8, textvariable=self.pl_mag).pack(side="left")
        ttk.Entry(pl_frame, width=6, textvariable=self.pl_x).pack(side="left", padx=2)
        ttk.Entry(pl_frame, width=4, textvariable=self.pl_ang).pack(side="left", padx=2)
        ttk.Button(left, text="Adicionar POINT", command=self._on_add_point).pack(fill="x", pady=(2, 8))

        # Carga UDL
        ttk.Label(left, text="Carga Distribuída (N/m de x1 a x2)").pack(anchor="w")
        udl_frame = ttk.Frame(left)
        udl_frame.pack(fill="x", pady=2)
        self.udl_w = tk.StringVar(value="500")
        self.udl_x1 = tk.StringVar(value="1.0")
        self.udl_x2 = tk.StringVar(value="4.0")
        ttk.Entry(udl_frame, width=8, textvariable=self.udl_w).pack(side="left")
        ttk.Entry(udl_frame, width=6, textvariable=self.udl_x1).pack(side="left", padx=2)
        ttk.Entry(udl_frame, width=6, textvariable=self.udl_x2).pack(side="left", padx=2)
        ttk.Button(left, text="Adicionar UDL", command=self._on_add_udl).pack(fill="x", pady=(2, 8))

        # Lista de cargas
        ttk.Label(left, text="Cargas adicionadas").pack(anchor="w", pady=(8, 2))
        self.loads_list = tk.Listbox(left, height=10)
        self.loads_list.pack(fill="x")
        ttk.Button(left, text="Remover Selecionada", command=self._on_remove_load).pack(fill="x", pady=(4, 8))

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=6)

        # Persistência
        save_frame = ttk.Frame(left)
        save_frame.pack(fill="x", pady=(4, 0))
        ttk.Label(save_frame, text="Projeto ID:").grid(row=0, column=0, sticky="w")
        ttk.Label(save_frame, text="Nome:").grid(row=1, column=0, sticky="w")
        self.proj_id = tk.StringVar(value="demo")
        self.proj_name = tk.StringVar(value="Exemplo")
        ttk.Entry(save_frame, textvariable=self.proj_id).grid(row=0, column=1, sticky="ew", padx=2, pady=1)
        ttk.Entry(save_frame, textvariable=self.proj_name).grid(row=1, column=1, sticky="ew", padx=2, pady=1)
        save_frame.columnconfigure(1, weight=1)

        btns = ttk.Frame(left)
        btns.pack(fill="x", pady=4)
        ttk.Button(btns, text="Salvar", command=self._on_save).pack(side="left", expand=True, fill="x", padx=1)
        ttk.Button(btns, text="Carregar", command=self._on_load).pack(side="left", expand=True, fill="x", padx=1)

        # ============ Canvas da barra ============ #
        self.canvas = tk.Canvas(right, background="#ffffff")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._render())

        self._refresh_loads_list()

    # ---------- Handlers ----------
    def _on_set_length(self):
        try:
            L = float(self.len_var.get())
            self.controller.set_length(L)
            self._render()
        except ValueError:
            messagebox.showerror("Erro", "Comprimento inválido.")

    def _on_add_point(self):
        try:
            m = float(self.pl_mag.get())
            x = float(self.pl_x.get())
            a = float(self.pl_ang.get())
            self.controller.add_point_load(m, x, a)
            self._refresh_loads_list()
            self._render()
        except ValueError:
            messagebox.showerror("Erro", "Dados de POINT inválidos.")

    def _on_add_udl(self):
        try:
            w = float(self.udl_w.get())
            x1 = float(self.udl_x1.get())
            x2 = float(self.udl_x2.get())
            self.controller.add_udl(w, x1, x2)
            self._refresh_loads_list()
            self._render()
        except ValueError:
            messagebox.showerror("Erro", "Dados de UDL inválidos.")

    def _on_remove_load(self):
        sel = self.loads_list.curselection()
        if not sel:
            return
        idx = int(sel[0])
        self.controller.remove_load(idx)
        self._refresh_loads_list()
        self._render()

    def _on_save(self):
        pid = self.proj_id.get().strip()
        name = self.proj_name.get().strip()
        if not pid or not name:
            messagebox.showerror("Erro", "Informe ID e Nome do projeto.")
            return
        self.controller.save(pid, name)
        messagebox.showinfo("OK", "Projeto salvo.")

    def _on_load(self):
        pid = self.proj_id.get().strip()
        data = self.controller.load(pid)
        if not data:
            messagebox.showwarning("Atenção", "Projeto não encontrado.")
            return
        self.len_var.set(str(self.controller.beam.length_m))
        self._refresh_loads_list()
        self._render()
        messagebox.showinfo("OK", f"Projeto '{data['name']}' carregado.")

    # ---------- Utilidades ----------
    def _refresh_loads_list(self):
        self.loads_list.delete(0, "end")
        for i, l in enumerate(self.controller.beam.loads):
            if l.kind == "POINT":
                txt = f"[{i}] POINT: {l.magnitude} N @ x={l.x} m  (ang={l.angle_deg}°)"
            else:
                txt = f"[{i}] UDL: {l.magnitude} N/m de {l.x1} a {l.x2} m"
            self.loads_list.insert("end", txt)

    def _render(self):
        self.adapter.render(self.canvas, self.controller.beam)

    def _toggle_sidebar(self):
        # lê posição atual e alterna
        try:
            cur = self.pw.sashpos(0)
        except Exception:
            cur = 260

        if not self._sidebar_collapsed:
            self._saved_sash = cur
            self.pw.sashpos(0, 0)
            self._sidebar_collapsed = True
            self._btn_toggle.config(text="⟩ Mostrar painel")
        else:
            self.pw.sashpos(0, self._saved_sash if self._saved_sash else 260)
            self._sidebar_collapsed = False
            self._btn_toggle.config(text="⟨ Ocultar painel")

        self._render()

    def _enforce_min_sizes(self, *_):
        # impede que a sidebar fique <220px ou o canvas <320px
        try:
            min_left, min_right = 220, 320
            total = max(self.pw.winfo_width(), min_left + min_right + 1)
            sash = self.pw.sashpos(0)
            sash = max(min_left, min(total - min_right, sash))
            self.pw.sashpos(0, sash)
        except Exception:
            pass