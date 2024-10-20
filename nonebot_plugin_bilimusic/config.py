from pydantic import BaseModel


class Config(BaseModel):
    bilimusic_limit: int = 2
    bilimusic_cookie: str = ''
