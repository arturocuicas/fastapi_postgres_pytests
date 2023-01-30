from pydantic import BaseModel


class BandRead(BaseModel):
    name: str
    song: str
