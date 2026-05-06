from pydantic import BaseModel


class RadarMetricResponse(BaseModel):
    asset_id: int
    complexity: float
    dominance: float
    density: float
    balance: float
    modularity: float

    class Config:
        from_attributes = True
