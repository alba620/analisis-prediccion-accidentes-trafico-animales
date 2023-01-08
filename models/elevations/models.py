from pydantic import BaseModel

class Sheet_data(BaseModel):
    sheet: str
    filename: str
    epsg: str