from dataclasses import dataclass, field
from typing import List, Literal, Optional

LoadType = Literal["POINT", "UDL"]

@dataclass
class Load:
    kind: LoadType
    magnitude: float  # N (POINT) ou N/m (UDL)
    x: Optional[float] = None  # posição (m) para POINT
    angle_deg: float = 270.0   # 270° = para baixo (eixo y positivo para baixo na tela)
    x1: Optional[float] = None # início UDL (m)
    x2: Optional[float] = None # fim UDL (m)

    def label(self) -> str:
        if self.kind == "POINT":
            return f"POINT: {self.magnitude:.2f} N @ x={self.x:.2f} m, θ={self.angle_deg:.1f}°"
        else:
            return f"UDL: {self.magnitude:.2f} N/m de {self.x1:.2f} a {self.x2:.2f} m"

@dataclass
class BeamModel:
    length_m: float = 5.0
    loads: List[Load] = field(default_factory=list)

    # ---- Placeholders para futura análise estrutural ----
    def reactions(self):
        return None

    def shear_function(self):
        return None

    def moment_function(self):
        return None
