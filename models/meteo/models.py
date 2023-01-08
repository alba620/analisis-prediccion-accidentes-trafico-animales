from pydantic import BaseModel

class aemet_data(BaseModel):
    fecha: str
    indicativo: str
    nombre: str
    provincia: str
    altitud: int
    tmed: float
    prec: float
    tmin: float
    tmax: float
    dir: str
    velmedia: float
    racha: float
    sol: float
    presMax: float
    presMin: float
    horatmin: str
    horatmax: str