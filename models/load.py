from dataclasses import dataclass
from typing import Literal, Optional

LoadType = Literal["POINT", "UDL"]

@dataclass
class Load:
    kind: LoadType
    magnitude: float           # N (POINT) ou N/m (UDL)
    x: Optional[float] = None  # posição (POINT)
    x1: Optional[float] = None # início (UDL)
    x2: Optional[float] = None # fim (UDL)
    angle_deg: float = 90.0    # só usado se POINT