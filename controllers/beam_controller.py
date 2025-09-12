from app.models.beam import Beam
from app.models.load import Load
from app.dao.sqlite_dao import SQLiteProjectDAO

class BeamController:
    def __init__(self, beam: Beam, dao=None):
        self.beam = beam
        self.dao = dao or SQLiteProjectDAO()

    # camada de orquestração entre View e Model
    def set_length(self, L: float):
        self.beam.length_m = L

    def add_point_load(self, magnitude: float, x: float, angle_deg: float = 90.0):
        self.beam.add_load(Load(kind="POINT", magnitude=magnitude, x=x, angle_deg=angle_deg))

    def add_udl(self, w: float, x1: float, x2: float):
        self.beam.add_load(Load(kind="UDL", magnitude=w, x1=x1, x2=x2))

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
        return data