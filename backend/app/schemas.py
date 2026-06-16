from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    identifier: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_name: str


class HotelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    price_avg: float
    rating: float
    neighborhood: str
    client_type: str
    latitude: float
    longitude: float
    image_url: str
    province: str = "Casablanca"
    rooms: int = 0
    beds: int = 0


class AirbnbOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    property_id: str | None = None
    name: str
    property_type: str
    price: float
    rating: float
    neighborhood: str
    latitude: float
    longitude: float
    temporal_demand: float
    image_url: str
    month: str | None = None
    price_tier: str | None = None
    bedrooms: float | None = None
    revenue: float | None = None
    distance_m: float | None = None
    relation: str | None = None


class CriterionOut(BaseModel):
    label: str
    competition_points: int
    complementarity_points: int


class PeriodOut(BaseModel):
    label: str
    competition: int
    complementarity: int


class HotelAnalysisOut(BaseModel):
    hotel: HotelOut
    radius_m: int
    airbnb_count: int
    avg_airbnb_price: float
    price_gap_percent: float
    competition_score: int
    complementarity_score: int
    relation: str
    criteria: list[CriterionOut]
    periods: list[PeriodOut]
    nearby_airbnbs: list[AirbnbOut]
