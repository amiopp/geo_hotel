from .database import SessionLocal
from .hotel_photos import REAL_HOTEL_PHOTOS
from .models import Hotel


def apply_hotel_photos() -> int:
    db = SessionLocal()
    updated = 0
    try:
        for hotel_id, photo in REAL_HOTEL_PHOTOS.items():
            hotel = db.get(Hotel, hotel_id)
            if hotel is None:
                continue
            if hotel.image_url != photo.image_url:
                hotel.image_url = photo.image_url
                updated += 1
        db.commit()
        return updated
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> None:
    updated = apply_hotel_photos()
    print(f"{updated} photos d'hotels mises a jour.")


if __name__ == "__main__":
    main()
