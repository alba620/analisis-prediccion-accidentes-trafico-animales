from pydantic import BaseModel

class Incidence(BaseModel):
    id: int
    prov: str
    road: str
    pk:float
    lon: float
    lat: float
    geom: str

