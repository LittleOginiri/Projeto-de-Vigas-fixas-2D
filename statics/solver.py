<<<<<<< HEAD
from typing import Callable, Tuple, List
from models.models import BeamModel, Load

def solve_reactions(model: BeamModel) -> Tuple[float, float]:
    """
    Calcula reações RA e RB para viga biapoiada em x=0 e x=L.
    (Implementação futura: somatório de forças e momentos,
     convertendo UDL em carga equivalente, etc.)
    """
    # TODO: implementação real
    return (0.0, 0.0)

def shear_function(model: BeamModel) -> Callable[[float], float]:
    """
    Retorna V(x) (função de esforço cortante) como callable.
    """
    # TODO: implementação real
    def V(x: float) -> float:
        return 0.0
    return V

def moment_function(V: Callable[[float], float]) -> Callable[[float], float]:
    """
    Retorna M(x) integrando V(x).
    """
    # TODO: implementação real (por partes, ou numérica)
    def M(x: float) -> float:
        return 0.0
    return M
=======
# statics/solver.py
from __future__ import annotations
from typing import List, Dict
import math
from models.load import Load

def _components_from_point(load: Load) -> tuple[float, float]:
    """
    Retorna (Fx, Fy) da carga pontual no sistema global.
    Convenção:
      • Ângulo medido a partir do +x, anti-horário (como na UI).
      • 90° = força vertical para BAIXO.
    Sinal adotado: Fy é NEGATIVO quando a carga aponta para baixo.
    """
    theta = math.radians(load.angle_deg)
    Fx = load.magnitude * math.cos(theta)
    Fy = -load.magnitude * math.sin(theta)
    return Fx, Fy

def _equivalent_from_udl(load: Load) -> tuple[float, float]:
    """
    Converte UDL (N/m, de x1 a x2) em carga equivalente para BAIXO:
      F_eq = w * (x2 - x1)  em x_eq = (x1 + x2)/2
    Retorna (F_eq_down, x_eq). F_eq_down é POSITIVA para baixo.
    """
    w = float(load.magnitude)
    a = float(load.x1)
    b = float(load.x2)
    Lseg = max(0.0, b - a)
    F_down = w * Lseg
    x_eq = a + Lseg/2.0
    return F_down, x_eq

def reactions(L: float, loads: List[Load]) -> Dict[str, float]:
    """
    Reações em viga biapoiada: pino em A (x=0) e rolete em B (x=L).
    Retorna: {'Ax','Ay','Bx','By'}
    Suporta POINT (qualquer ângulo) e UDL.
    """
    sum_Fx = 0.0          # soma dos Fx das cargas
    sum_Fy = 0.0          # positiva para CIMA (logo, cargas para baixo entram negativas)
    sum_MA = 0.0          # momento em torno de A (CCW positivo)

    for ld in loads:
        if ld.kind == "POINT":
            Fx, Fy = _components_from_point(ld)  # Fy negativo (baixo) para θ=90°
            sum_Fx += Fx
            sum_Fy += Fy
            sum_MA += Fy * float(ld.x)
        else:  # UDL
            F_down, x_eq = _equivalent_from_udl(ld)  # F_down > 0 (para baixo)
            Fy = -F_down                             # converter para nosso sinal (baixo = negativo)
            sum_Fy += Fy
            sum_MA += Fy * x_eq

    # Horizontal: rolete não reage em X → Bx = 0; pino fecha equilíbrio
    Bx = 0.0
    Ax = -sum_Fx

    # Vertical + momento:
    #  ΣM_A = 0 → By*L + Σ(Fy_i*x_i) = 0  → By = -ΣM_A/L  (Fy<0 p/baixo)
    #  ΣFy = 0 → Ay + By + ΣFy = 0         → Ay = -ΣFy - By
    L_safe = max(float(L), 1e-9)
    By = -sum_MA / L_safe
    Ay = -sum_Fy - By

    return {"Ax": Ax, "Ay": Ay, "Bx": Bx, "By": By}
>>>>>>> 80e0cdd (.)
