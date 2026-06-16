from math import asin, cos, radians, sin, sqrt
from secrets import compare_digest

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from .database import Base, engine, get_db, settings
from .models import Airbnb, AirbnbMonthly, Hotel
from .schemas import AirbnbOut, CriterionOut, HotelAnalysisOut, HotelOut, LoginRequest, LoginResponse, PeriodOut
from .seed import seed_database

app = FastAPI(title="GeoHotel Insight API", version="1.0.0")

LOCAL_DEV_ORIGIN_REGEX = (
    r"^https?://("
    r"localhost|127\.0\.0\.1|0\.0\.0\.0|"
    r"192\.168\.\d{1,3}\.\d{1,3}|"
    r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r")(:\d+)?$"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_origin_regex=LOCAL_DEV_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_runtime_indexes()
    db = next(get_db())
    try:
        seed_database(db)
    finally:
        db.close()


def ensure_runtime_indexes() -> None:
    statements = [
        "CREATE INDEX IF NOT EXISTS ix_airbnbs_lat_lon ON airbnbs (latitude, longitude)",
        "CREATE INDEX IF NOT EXISTS ix_airbnb_monthly_lat_lon ON airbnb_monthly (latitude, longitude)",
        "CREATE INDEX IF NOT EXISTS ix_airbnb_monthly_month_lat_lon ON airbnb_monthly (month, latitude, longitude)",
    ]
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    earth_radius_m = 6_371_000
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)
    a = sin(delta_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(delta_lon / 2) ** 2
    return 2 * earth_radius_m * asin(sqrt(a))


def clamp_score(value: float) -> int:
    return max(0, min(100, round(value)))


def relation_label(score: int) -> str:
    if score >= 76:
        return "Concurrence forte"
    if score >= 58:
        return "Concurrence moyenne"
    if score >= 42:
        return "Relation mixte"
    return "Complémentarité dominante"


def month_label(month: str) -> str:
    month_names = {
        "01": "janv.",
        "02": "févr.",
        "03": "mars",
        "04": "avr.",
        "05": "mai",
        "06": "juin",
        "07": "juil.",
        "08": "août",
        "09": "sept.",
        "10": "oct.",
        "11": "nov.",
        "12": "déc.",
    }
    if "-" not in month:
        return month
    year, month_number = month.split("-", 1)
    return f"{month_names.get(month_number, month_number)} {year[-2:]}"


def fallback_periods(competition_score: int, complementarity_score: int) -> list[PeriodOut]:
    return [
        PeriodOut(label="1 mars", competition=clamp_score(competition_score - 6), complementarity=clamp_score(complementarity_score - 4)),
        PeriodOut(label="15 mars", competition=clamp_score(competition_score - 4), complementarity=clamp_score(complementarity_score - 2)),
        PeriodOut(label="1 avr.", competition=clamp_score(competition_score + 7), complementarity=clamp_score(complementarity_score + 4)),
        PeriodOut(label="15 avr.", competition=clamp_score(competition_score + 13), complementarity=clamp_score(complementarity_score + 6)),
        PeriodOut(label="1 mai", competition=clamp_score(competition_score + 2), complementarity=clamp_score(complementarity_score - 3)),
        PeriodOut(label="15 mai", competition=clamp_score(competition_score + 4), complementarity=clamp_score(complementarity_score + 1)),
    ]


def build_periods(
    hotel: Hotel,
    radius_m: int,
    monthly_rows: list[AirbnbMonthly],
    competition_score: int,
    complementarity_score: int,
) -> list[PeriodOut]:
    if not monthly_rows:
        return fallback_periods(competition_score, complementarity_score)

    rows_by_month: dict[str, list[AirbnbMonthly]] = {}
    for row in monthly_rows:
        distance = distance_meters(hotel.latitude, hotel.longitude, row.latitude, row.longitude)
        if distance <= radius_m:
            rows_by_month.setdefault(row.month, []).append(row)

    selected_months = sorted(rows_by_month)[-6:]
    if not selected_months:
        return fallback_periods(competition_score, complementarity_score)

    max_count = max(len(rows_by_month[month]) for month in selected_months) or 1
    periods: list[PeriodOut] = []
    for month in selected_months:
        rows = rows_by_month[month]
        avg_adr = sum(row.adr for row in rows) / len(rows)
        avg_occupancy = sum(row.occupancy for row in rows) / len(rows)
        price_gap = ((avg_adr - hotel.price_avg) / hotel.price_avg) * 100 if hotel.price_avg else 0
        density_pressure = (len(rows) / max_count) * 100
        price_pressure = 100 - min(abs(price_gap), 65) * 1.25
        occupancy_pressure = avg_occupancy * 100
        competition = clamp_score(density_pressure * 0.38 + price_pressure * 0.34 + occupancy_pressure * 0.28)
        complementarity = clamp_score(100 - competition + 12)
        periods.append(PeriodOut(label=month_label(month), competition=competition, complementarity=complementarity))
    return periods


def build_analysis(
    hotel: Hotel,
    airbnbs: list[Airbnb],
    radius_m: int,
    monthly_rows: list[AirbnbMonthly] | None = None,
) -> HotelAnalysisOut:
    nearby: list[tuple[Airbnb, float]] = []
    distances: list[float] = []
    for airbnb in airbnbs:
        distance = distance_meters(hotel.latitude, hotel.longitude, airbnb.latitude, airbnb.longitude)
        if distance <= radius_m:
            distances.append(distance)
            nearby.append((airbnb, distance))

    if not nearby:
        criteria = [
            CriterionOut(label="Distance", competition_points=0, complementarity_points=0),
            CriterionOut(label="Prix", competition_points=0, complementarity_points=0),
            CriterionOut(label="Type d'offre", competition_points=0, complementarity_points=0),
            CriterionOut(label="Temporalité", competition_points=0, complementarity_points=0),
        ]
        periods = [
            PeriodOut(label="1 mars", competition=0, complementarity=0),
            PeriodOut(label="15 mars", competition=0, complementarity=0),
            PeriodOut(label="1 avr.", competition=0, complementarity=0),
            PeriodOut(label="15 avr.", competition=0, complementarity=0),
            PeriodOut(label="1 mai", competition=0, complementarity=0),
            PeriodOut(label="15 mai", competition=0, complementarity=0),
        ]
        return HotelAnalysisOut(
            hotel=HotelOut.model_validate(hotel),
            radius_m=radius_m,
            airbnb_count=0,
            avg_airbnb_price=0,
            price_gap_percent=0,
            competition_score=0,
            complementarity_score=0,
            relation="Aucune donnée",
            criteria=criteria,
            periods=periods,
            nearby_airbnbs=[],
        )

    avg_price = sum(item.price for item, _ in nearby) / len(nearby)
    price_gap_percent = ((avg_price - hotel.price_avg) / hotel.price_avg) * 100 if hotel.price_avg else 0
    avg_distance = sum(distances) / len(distances)
    avg_temporal = sum(item.temporal_demand for item, _ in nearby) / len(nearby)

    distance_competition = clamp_score(100 - (avg_distance / radius_m) * 55)
    price_competition = clamp_score(100 - min(abs(price_gap_percent), 65) * 1.25)
    offer_competition = 64 if "Business" in hotel.client_type or "Affaires" in hotel.client_type else 50
    temporal_competition = clamp_score(avg_temporal * 100)

    competition_score = clamp_score(
        distance_competition * 0.32
        + price_competition * 0.28
        + offer_competition * 0.18
        + temporal_competition * 0.22
    )
    complementarity_score = clamp_score(
        (100 - distance_competition) * 0.22
        + (100 - price_competition) * 0.24
        + (100 - offer_competition) * 0.24
        + (100 - temporal_competition) * 0.30
        + 22
    )

    criteria = [
        CriterionOut(
            label="Distance",
            competition_points=distance_competition,
            complementarity_points=100 - distance_competition,
        ),
        CriterionOut(
            label="Prix",
            competition_points=price_competition,
            complementarity_points=100 - price_competition,
        ),
        CriterionOut(
            label="Type d'offre",
            competition_points=offer_competition,
            complementarity_points=100 - offer_competition,
        ),
        CriterionOut(
            label="Temporalité",
            competition_points=temporal_competition,
            complementarity_points=100 - temporal_competition,
        ),
    ]

    periods = build_periods(hotel, radius_m, monthly_rows or [], competition_score, complementarity_score)
    nearby_airbnbs = []
    for airbnb, distance in sorted(nearby, key=lambda item: item[1]):
        item = AirbnbOut.model_validate(airbnb)
        item.distance_m = round(distance)
        item.relation = "Concurrence forte" if abs(airbnb.price - hotel.price_avg) <= 130 and distance < 450 else (
            "Concurrence moyenne" if distance < radius_m * 0.65 else "Complémentarité"
        )
        nearby_airbnbs.append(item)

    return HotelAnalysisOut(
        hotel=HotelOut.model_validate(hotel),
        radius_m=radius_m,
        airbnb_count=len(nearby),
        avg_airbnb_price=round(avg_price),
        price_gap_percent=round(price_gap_percent, 1),
        competition_score=competition_score,
        complementarity_score=complementarity_score,
        relation=relation_label(competition_score),
        criteria=criteria,
        periods=periods,
        nearby_airbnbs=nearby_airbnbs,
    )


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "app": "GeoHotel Insight API",
        "status": "ok",
        "frontend": "http://localhost:5192",
        "health": "/api/health",
        "docs": "/docs",
    }


@app.post("/api/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    identifier_ok = compare_digest(payload.identifier.strip(), settings.login_identifier)
    password_ok = compare_digest(payload.password, settings.login_password)
    if not identifier_ok or not password_ok:
        raise HTTPException(status_code=401, detail="Identifiant ou mot de passe incorrect")
    return LoginResponse(access_token=settings.login_token, user_name=settings.login_display_name)


def require_session(authorization: str | None = Header(default=None)) -> None:
    scheme, _, token = (authorization or "").partition(" ")
    token_ok = scheme.lower() == "bearer" and compare_digest(token, settings.login_token)
    if not token_ok:
        raise HTTPException(status_code=401, detail="Session invalide ou expirée")


@app.get("/api/hotels", response_model=list[HotelOut])
def list_hotels(_: None = Depends(require_session), db: Session = Depends(get_db)) -> list[Hotel]:
    return db.query(Hotel).order_by(Hotel.id).all()


@app.get("/api/airbnbs", response_model=list[AirbnbOut])
def list_airbnbs(_: None = Depends(require_session), db: Session = Depends(get_db)) -> list[Airbnb]:
    return db.query(Airbnb).order_by(Airbnb.id).all()


@app.get("/api/hotels/{hotel_id}/analysis", response_model=HotelAnalysisOut)
def get_hotel_analysis(
    hotel_id: int,
    radius_m: int = Query(1000, ge=500, le=5000),
    _: None = Depends(require_session),
    db: Session = Depends(get_db),
) -> HotelAnalysisOut:
    hotel = db.get(Hotel, hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hôtel introuvable")

    query_radius_m = radius_m + 120
    lat_delta = query_radius_m / 111_000
    lon_delta = query_radius_m / (111_000 * max(0.2, cos(radians(hotel.latitude))))
    airbnbs = (
        db.query(Airbnb)
        .filter(Airbnb.latitude.between(hotel.latitude - lat_delta, hotel.latitude + lat_delta))
        .filter(Airbnb.longitude.between(hotel.longitude - lon_delta, hotel.longitude + lon_delta))
        .order_by(Airbnb.id)
        .all()
    )
    recent_months = [
        month
        for (month,) in (
            db.query(AirbnbMonthly.month)
            .distinct()
            .order_by(AirbnbMonthly.month.desc())
            .limit(6)
            .all()
        )
    ]
    monthly_query = (
        db.query(AirbnbMonthly)
        .filter(AirbnbMonthly.latitude.between(hotel.latitude - lat_delta, hotel.latitude + lat_delta))
        .filter(AirbnbMonthly.longitude.between(hotel.longitude - lon_delta, hotel.longitude + lon_delta))
    )
    if recent_months:
        monthly_query = monthly_query.filter(AirbnbMonthly.month.in_(recent_months))
    monthly_rows = monthly_query.all()
    return build_analysis(hotel, airbnbs, radius_m, monthly_rows)
