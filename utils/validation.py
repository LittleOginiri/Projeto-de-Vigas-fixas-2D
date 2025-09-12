from models.models import BeamModel

def validate_point(model: BeamModel, x: float):
    L = model.length_m
    assert 0.0 <= x <= L, f"x deve estar entre 0 e {L:.2f} m"

def validate_interval(model: BeamModel, x1: float, x2: float):
    L = model.length_m
    assert 0.0 <= x1 < x2 <= L, f"Intervalo deve estar dentro de [0, {L:.2f}] e com x1<x2"