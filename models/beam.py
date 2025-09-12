from dataclasses import dataclass, field
from typing import List
from .load import Load

@dataclass
class Beam:
    length_m: float
    loads: List[Load] = field(default_factory=list)

    def add_load(self, load: Load) -> None:
        self.loads.append(load)

    def remove_load(self, idx: int) -> None:
        del self.loads[idx]