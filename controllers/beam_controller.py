from models.beam import Beam
from models.load import Load
from dao.sqlite_dao import SQLiteProjectDAO

class BeamController:
    def __init__(self, beam: Beam | None = None, dao=None):
        self.beam = beam or Beam()
        self.dao = dao or SQLiteProjectDAO()

    # ações de edição
    def set_length(self, L: float):
        self.beam.length_m = max(0.01, float(L))

    def add_point_load(self, magnitude: float, x: float, angle_deg: float = 90.0):
        self.beam.add_load(Load(kind="POINT", magnitude=float(magnitude), x=float(x), angle_deg=float(angle_deg)))

    def add_udl(self, w: float, x1: float, x2: float):
        x1, x2 = float(x1), float(x2)
        if x1 > x2:
            x1, x2 = x2, x1
        self.beam.add_load(Load(kind="UDL", magnitude=float(w), x1=x1, x2=x2))

    def remove_load(self, idx: int):
        self.beam.remove_load(idx)

    # persistência
    def save(self, project_id: str, name: str):
        payload = {
            "id": project_id,
            "name": name,
            "beam": {
                "length_m": self.beam.length_m,
                "loads": [l.__dict__ for l in self.beam.loads],
            },
        }
        self.dao.save_project(payload)

    def load(self, project_id: str):
        data = self.dao.load_project(project_id)
        if not data:
            return None
        self.beam.length_m = data["beam"]["length_m"]
        self.beam.loads.clear()
        for l in data["beam"]["loads"]:
            self.beam.add_load(Load(**l))
        return data