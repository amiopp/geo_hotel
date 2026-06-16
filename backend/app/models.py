from sqlalchemy import Float, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    category: Mapped[str] = mapped_column(String(40), nullable=False)
    price_avg: Mapped[float] = mapped_column(Float, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    neighborhood: Mapped[str] = mapped_column(String(80), nullable=False)
    client_type: Mapped[str] = mapped_column(String(80), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    province: Mapped[str] = mapped_column(String(80), nullable=False, default="Casablanca")
    rooms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    beds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class Airbnb(Base):
    __tablename__ = "airbnbs"
    __table_args__ = (
        Index("ix_airbnbs_lat_lon", "latitude", "longitude"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    property_id: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    property_type: Mapped[str] = mapped_column(String(80), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    neighborhood: Mapped[str] = mapped_column(String(80), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    temporal_demand: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    month: Mapped[str] = mapped_column(String(7), nullable=False, default="")
    price_tier: Mapped[str] = mapped_column(String(40), nullable=False, default="")
    bedrooms: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    revenue: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    stability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    territorial_score: Mapped[float] = mapped_column(Float, nullable=False, default=0)


class AirbnbMonthly(Base):
    __tablename__ = "airbnb_monthly"
    __table_args__ = (
        UniqueConstraint("property_id", "month", name="uq_airbnb_monthly_property_month"),
        Index("ix_airbnb_monthly_lat_lon", "latitude", "longitude"),
        Index("ix_airbnb_monthly_month_lat_lon", "month", "latitude", "longitude"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    property_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    month: Mapped[str] = mapped_column(String(7), nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    active: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    adr: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    occupancy: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    revenue: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    revenue_potential: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    bedrooms: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    price_tier: Mapped[str] = mapped_column(String(40), nullable=False, default="")
    rating_overall: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    rating_location: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    stability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    territorial_score: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    final_selection_score: Mapped[float] = mapped_column(Float, nullable=False, default=0)
