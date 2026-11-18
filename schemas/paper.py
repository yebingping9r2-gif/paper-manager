from pydantic import BaseModel

class PaperCreate(BaseModel):
    title: str
    author: str | None = None
    publish_year: int | None = None
    abstract: str | None = None

class PaperUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    publish_year: int | None = None
    abstract: str | None = None
