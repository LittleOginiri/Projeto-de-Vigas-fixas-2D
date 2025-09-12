from typing import Any
from .renderer import BeamRenderer

class RenderAdapter:
    def __init__(self):
        self._inst = None

    def render(self, canvas: Any, beam: Any) -> None:
        # instancia uma vez por canvas
        if self._inst is None:
            self._inst = BeamRenderer(canvas)

        # chama a API pública do seu renderer
        L = getattr(beam, "length_m", 0.0)
        loads = getattr(beam, "loads", [])
        self._inst.draw_scene(L, loads)