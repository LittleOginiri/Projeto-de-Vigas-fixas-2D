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