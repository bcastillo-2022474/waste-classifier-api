from pydantic import BaseModel

class StatsWasteItem(BaseModel):
    material: str
    count: int

    class Config:
        extra = "ignore"
        allow_mutations = False
    def __getitem__(self, item):
        return getattr(self, item)