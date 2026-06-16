import argparse
import csv
import io
import re
import zipfile
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .hotel_photos import hotel_image_for
from .models import Airbnb, AirbnbMonthly, Hotel

HOTELS_CSV = "pfe/hotels/hotels_complet_avec_prix_FINAL.csv"
AIRBNB_CSV = "pfe/airbnb/airbnb_reconstruction_corrigee_spatialement__5_ (1).csv"

AIRBNB_IMAGES = {
    "budget": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=300&q=70",
    "economy": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=300&q=70",
    "midscale": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=300&q=70",
    "upscale": "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=300&q=70",
    "luxury": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=300&q=70",
}


def to_float(value: Any, default: float = 0) -> float:
    if value is None:
        return default
    text = str(value).strip().replace(",", ".")
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return default


def to_int(value: Any, default: int = 0) -> int:
    return int(round(to_float(value, default)))


def clean_text(value: Any) -> str:
    text = str(value or "").strip()
    return text.replace("H?tel", "Hôtel").replace("D?nomina", "Dénomination")


def star_count(category: str) -> int:
    match = re.search(r"(\d)\s*\*", category)
    if not match:
        match = re.search(r"(\d)", category)
    return int(match.group(1)) if match else 3


def hotel_category(raw_category: str) -> str:
    stars = star_count(raw_category)
    return f"{stars} étoile" if stars == 1 else f"{stars} étoiles"


def hotel_rating(raw_category: str) -> float:
    stars = star_count(raw_category)
    return {1: 3.2, 2: 3.5, 3: 3.9, 4: 4.3, 5: 4.7}.get(stars, 4.0)


def hotel_client_type(raw_category: str, rooms: int) -> str:
    stars = star_count(raw_category)
    if stars >= 5:
        return "Luxe / Tourisme"
    if stars >= 4 or rooms >= 80:
        return "Business / Tourisme"
    if rooms <= 30:
        return "Court séjour / Budget"
    return "Tourisme / Affaires"


def infer_neighborhood(latitude: float, longitude: float) -> str:
    if longitude < -7.66:
        return "Ain Diab"
    if latitude > 33.598 and longitude < -7.61:
        return "Casa Port"
    if longitude < -7.635:
        return "Maarif / Racine"
    if latitude < 33.565:
        return "Sidi Maarouf"
    if latitude < 33.58:
        return "Gauthier / Palmier"
    return "Centre-ville"


def property_type(bedrooms: float) -> str:
    if bedrooms <= 0:
        return "Studio"
    if bedrooms == 1:
        return "Appartement 1 chambre"
    return f"Appartement {int(round(bedrooms))} chambres"


def rating_from_overall(value: float) -> float:
    if value > 10:
        return round(max(0, min(5, value / 20)), 1)
    return round(max(0, min(5, value / 2)), 1)


def active_to_int(value: Any) -> int:
    text = str(value or "").strip().lower()
    return 1 if text in {"1", "true", "vrai", "yes", "oui"} else 0


def read_hotels(zf: zipfile.ZipFile) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with zf.open(HOTELS_CSV) as raw:
        reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace", newline=""), delimiter=";")
        for index, row in enumerate(reader, start=1):
            name = clean_text(row.get("D?nomina")) or f"Hôtel {index}"
            raw_category = clean_text(row.get("Type et Ca"))
            latitude = to_float(row.get("latitude"))
            longitude = to_float(row.get("longitude"))
            rooms = to_int(row.get("chambres"))
            beds = to_int(row.get("lits"))
            rows.append(
                {
                    "id": index,
                    "name": name.title(),
                    "category": hotel_category(raw_category),
                    "price_avg": to_float(row.get("ADR hotel")),
                    "rating": hotel_rating(raw_category),
                    "neighborhood": infer_neighborhood(latitude, longitude),
                    "client_type": hotel_client_type(raw_category, rooms),
                    "latitude": latitude,
                    "longitude": longitude,
                    "image_url": hotel_image_for(index),
                    "province": clean_text(row.get("Province/P")) or "Casablanca",
                    "rooms": rooms,
                    "beds": beds,
                }
            )
    return rows


def airbnb_monthly_mapping(row: dict[str, str]) -> dict[str, Any]:
    return {
        "property_id": row.get("property_id") or "",
        "month": row.get("mois") or "",
        "latitude": to_float(row.get("latitude")),
        "longitude": to_float(row.get("longitude")),
        "active": active_to_int(row.get("actif")),
        "adr": to_float(row.get("adr")),
        "occupancy": to_float(row.get("occupancy")),
        "revenue": to_float(row.get("revenue")),
        "revenue_potential": to_float(row.get("revenue_potential")),
        "bedrooms": to_float(row.get("bedrooms")),
        "price_tier": clean_text(row.get("price_tier")).lower(),
        "rating_overall": to_float(row.get("rating_overall")),
        "rating_location": to_float(row.get("rating_location")),
        "stability_score": to_float(row.get("stability_score")),
        "territorial_score": to_float(row.get("territorial_score")),
        "final_selection_score": to_float(row.get("final_selection_score")),
    }


def airbnb_listing_mapping(row: dict[str, Any], index: int) -> dict[str, Any]:
    tier = row.get("price_tier") or "midscale"
    bedrooms = to_float(row.get("bedrooms"))
    property_id = row.get("property_id") or f"airbnb_{index}"
    suffix = property_id.split("_")[-1][-6:]
    return {
        "id": index,
        "property_id": property_id,
        "name": f"Airbnb {suffix}",
        "property_type": property_type(bedrooms),
        "price": to_float(row.get("adr")),
        "rating": rating_from_overall(to_float(row.get("rating_overall"))),
        "neighborhood": clean_text(tier).title() or "Casablanca",
        "latitude": to_float(row.get("latitude")),
        "longitude": to_float(row.get("longitude")),
        "temporal_demand": to_float(row.get("occupancy")),
        "image_url": AIRBNB_IMAGES.get(tier, AIRBNB_IMAGES["midscale"]),
        "month": row.get("month") or "",
        "price_tier": tier,
        "bedrooms": bedrooms,
        "revenue": to_float(row.get("revenue")),
        "stability_score": to_float(row.get("stability_score")),
        "territorial_score": to_float(row.get("territorial_score")),
    }


def import_archive(zip_path: Path, recreate: bool = True) -> dict[str, int]:
    if not zip_path.exists():
        raise FileNotFoundError(f"Archive introuvable: {zip_path}")

    if recreate:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    latest_by_property: dict[str, dict[str, Any]] = {}
    monthly_count = 0
    try:
        with zipfile.ZipFile(zip_path) as zf:
            hotels = read_hotels(zf)
            db.bulk_insert_mappings(Hotel, hotels)

            batch: list[dict[str, Any]] = []
            with zf.open(AIRBNB_CSV) as raw:
                reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace", newline=""))
                for row in reader:
                    monthly = airbnb_monthly_mapping(row)
                    if not monthly["property_id"] or not monthly["month"]:
                        continue
                    batch.append(monthly)
                    monthly_count += 1

                    current = latest_by_property.get(monthly["property_id"])
                    if current is None or monthly["month"] > current.get("month", ""):
                        latest_by_property[monthly["property_id"]] = monthly

                    if len(batch) >= 5000:
                        db.bulk_insert_mappings(AirbnbMonthly, batch)
                        db.commit()
                        batch.clear()

            if batch:
                db.bulk_insert_mappings(AirbnbMonthly, batch)
                db.commit()

        listings = [
            airbnb_listing_mapping(row, index)
            for index, row in enumerate(sorted(latest_by_property.values(), key=lambda item: item["property_id"]), start=1)
        ]
        db.bulk_insert_mappings(Airbnb, listings)
        db.commit()
        return {"hotels": len(hotels), "airbnb_listings": len(listings), "airbnb_monthly_rows": monthly_count}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Importe les données GeoHotel Insight depuis l'archive PFE.")
    parser.add_argument("--zip", required=True, type=Path, help="Chemin vers pfe-*.zip")
    parser.add_argument("--no-recreate", action="store_true", help="N'efface pas les tables avant import.")
    args = parser.parse_args()

    result = import_archive(args.zip, recreate=not args.no_recreate)
    print(
        "Import terminé: "
        f"{result['hotels']} hôtels, "
        f"{result['airbnb_listings']} Airbnb uniques, "
        f"{result['airbnb_monthly_rows']} lignes mensuelles."
    )


if __name__ == "__main__":
    main()
