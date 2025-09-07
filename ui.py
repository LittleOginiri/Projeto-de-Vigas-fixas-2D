# ui.py
import tkinter as tk
from tkinter import ttk

class BeamUI(ttk.Frame):
    """
    Responsável apenas por CRIAR a interface:
      - campos/controles do painel esquerdo
      - lista de cargas
      - canvas de desenho
    Não contém regras de negócio; aciona callbacks fornecidos pelo app.
    """
    def __init__(self, master, model, *,
                 on_length_change,
                 on_add_load,
                 on_remove_selected,
                 on_clear_loads,
                 on_canvas_resize):
        super().__init__(master)
        self.model = model

        # ----------------- Variáveis públicas -----------------
        self.len_var      = tk.DoubleVar(value=self.model.length_m)
        self.kind_var     = tk.StringVar(value="POINT")
        self.point_F      = tk.DoubleVar(value=1000.0)
        self.point_x      = tk.DoubleVar(value=2.5)
        self.point_theta  = tk.DoubleVar(value=270.0)
        self.udl_w        = tk.DoubleVar(value=500.0)
        self.udl_x1       = tk.DoubleVar(value=1.0)
        self.udl_x2       = tk.DoubleVar(value=4.0)

        # Guardar callbacks
        self._on_length_change   = on_length_change
        self._on_add_load        = on_add_load
        self._on_remove_selected = on_remove_selected
        self._on_clear_loads     = on_clear_loads
        self._on_canvas_resize   = on_canvas_resize

        # Layout raiz
        self.pack(fill=tk.BOTH, expand=True)
        self._build(master)

    # ---------------------- Construção ----------------------
    def _build(self, master):
        root = self
        # Painel esquerdo: controles
        left = ttk.Frame(root, padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y)

        # Comprimento da viga
        lf_len = ttk.LabelFrame(left, text="Comprimento da viga (m)")
        lf_len.pack(fill=tk.X, pady=(0, 10))
        len_entry = ttk.Spinbox(
            lf_len, from_=0.5, to=100.0, increment=0.1,
            textvariable=self.len_var, width=10,
            command=self._on_length_change
        )
        len_entry.pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(lf_len, text="Aplicar", command=self._on_length_change)\
            .pack(side=tk.LEFT, padx=5)

        # Adicionar carga
        lf_add = ttk.LabelFrame(left, text="Adicionar carga")
        lf_add.pack(fill=tk.X, pady=(0, 10))

        # Tipo
        ttk.Label(lf_add, text="Tipo:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=4)
        kind_cb = ttk.Combobox(lf_add, textvariable=self.kind_var,
                               values=["POINT", "UDL"], width=8, state="readonly")
        kind_cb.grid(row=0, column=1, sticky=tk.W, padx=5, pady=4)
        kind_cb.bind("<<ComboboxSelected>>", lambda e: self.switch_load_inputs())

        # Campos para POINT
        self.point_frame = ttk.Frame(lf_add)
        ttk.Label(self.point_frame, text="F (N):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=4)
        ttk.Entry(self.point_frame, textvariable=self.point_F, width=10).grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(self.point_frame, text="x (m):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=4)
        ttk.Entry(self.point_frame, textvariable=self.point_x, width=10).grid(row=0, column=3, padx=5, pady=4)

        ttk.Label(self.point_frame, text="θ (°):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=4)
        ttk.Entry(self.point_frame, textvariable=self.point_theta, width=10).grid(row=1, column=1, padx=5, pady=4)

        # Campos para UDL
        self.udl_frame = ttk.Frame(lf_add)
        ttk.Label(self.udl_frame, text="w (N/m):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=4)
        ttk.Entry(self.udl_frame, textvariable=self.udl_w, width=10).grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(self.udl_frame, text="x1 (m):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=4)
        ttk.Entry(self.udl_frame, textvariable=self.udl_x1, width=10).grid(row=0, column=3, padx=5, pady=4)

        ttk.Label(self.udl_frame, text="x2 (m):").grid(row=0, column=4, sticky=tk.W, padx=5, pady=4)
        ttk.Entry(self.udl_frame, textvariable=self.udl_x2, width=10).grid(row=0, column=5, padx=5, pady=4)

        # Botões
        btns = ttk.Frame(lf_add)
        btns.grid(row=2, column=0, columnspan=6, sticky="w", pady=6)
        ttk.Button(btns, text="Adicionar", command=self._on_add_load).pack(side=tk.LEFT, padx=5)

        # Frame de campos específico do tipo
        self.point_frame.grid(row=1, column=0, columnspan=6, sticky="we")
        self.udl_frame.grid(row=1, column=0, columnspan=6, sticky="we")
        self.udl_frame.grid_remove()  # esconde UDL inicialmente

        # Lista de cargas
        lf_list = ttk.LabelFrame(left, text="Cargas")
        lf_list.pack(fill=tk.BOTH, expand=True)
        self.load_list = tk.Listbox(lf_list, height=12)
        self.load_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        list_btns = ttk.Frame(lf_list)
        list_btns.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(list_btns, text="Remover selecionada", command=self._on_remove_selected)\
            .pack(side=tk.LEFT, padx=5)
        ttk.Button(list_btns, text="Limpar tudo", command=self._on_clear_loads)\
            .pack(side=tk.LEFT, padx=5)

        # Painel direito: Canvas de desenho
        right = ttk.Frame(root, padding=(10, 10, 10, 10))
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(right, bg="#ffffff")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Redesenhar ao redimensionar
        self.canvas.bind("<Configure>", lambda e: self._on_canvas_resize())

    # ---------------------- Helpers públicos ----------------------
    def switch_load_inputs(self):
        """Alterna a exibição dos grupos de campos conforme o tipo da carga."""
        self.point_frame.grid_remove()
        self.udl_frame.grid_remove()
        if self.kind_var.get() == "POINT":
            self.point_frame.grid()
        else:
            self.udl_frame.grid()
