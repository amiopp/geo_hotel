from sqlalchemy.orm import Session

from .models import Airbnb, Hotel


HOTELS = [
    {
        "id": 1,
        "name": "Hôtel Atlas Center",
        "category": "4 étoiles",
        "price_avg": 750,
        "rating": 4.3,
        "neighborhood": "Centre-ville",
        "client_type": "Business / Tourisme",
        "latitude": 33.5899,
        "longitude": -7.6214,
        "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": 2,
        "name": "Hôtel Corniche Bleu",
        "category": "5 étoiles",
        "price_avg": 1180,
        "rating": 4.6,
        "neighborhood": "Ain Diab",
        "client_type": "Loisir / Luxe",
        "latitude": 33.5952,
        "longitude": -7.6743,
        "image_url": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": 3,
        "name": "Hôtel Maarif Urban",
        "category": "3 étoiles",
        "price_avg": 520,
        "rating": 4.0,
        "neighborhood": "Maarif",
        "client_type": "Affaires / Court séjour",
        "latitude": 33.5849,
        "longitude": -7.6424,
        "image_url": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": 4,
        "name": "Hôtel Casa Port",
        "category": "4 étoiles",
        "price_avg": 690,
        "rating": 4.1,
        "neighborhood": "Casa Port",
        "client_type": "Business / Transit",
        "latitude": 33.5991,
        "longitude": -7.6135,
        "image_url": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=900&q=80",
    },
]

AIRBNBS = [
    {
        "id": 1,
        "name": "Appartement Gauthier",
        "property_type": "Appartement entier",
        "price": 650,
        "rating": 4.8,
        "neighborhood": "Gauthier",
        "latitude": 33.5889,
        "longitude": -7.6206,
        "temporal_demand": 0.78,
        "image_url": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=300&q=70",
    },
    {
        "id": 2,
        "name": "Studio Les Fleurs",
        "property_type": "Studio",
        "price": 520,
        "rating": 4.5,
        "neighborhood": "Les Fleurs",
        "latitude": 33.5909,
        "longitude": -7.6185,
        "temporal_demand": 0.72,
        "image_url": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=300&q=70",
    },
    {
        "id": 3,
        "name": "Loft Maarif Central",
        "property_type": "Loft",
        "price": 700,
        "rating": 4.7,
        "neighborhood": "Maarif",
        "latitude": 33.5846,
        "longitude": -7.6232,
        "temporal_demand": 0.58,
        "image_url": "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=300&q=70",
    },
    {
        "id": 4,
        "name": "Suite Palmier",
        "property_type": "Suite privée",
        "price": 840,
        "rating": 4.9,
        "neighborhood": "Palmier",
        "latitude": 33.5816,
        "longitude": -7.6137,
        "temporal_demand": 0.51,
        "image_url": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=300&q=70",
    },
    {
        "id": 5,
        "name": "Chambre Twin Anfa",
        "property_type": "Chambre privée",
        "price": 390,
        "rating": 4.1,
        "neighborhood": "Anfa",
        "latitude": 33.5972,
        "longitude": -7.6289,
        "temporal_demand": 0.47,
        "image_url": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=300&q=70",
    },
    {
        "id": 6,
        "name": "Terrasse Centre Ville",
        "property_type": "Appartement entier",
        "price": 610,
        "rating": 4.6,
        "neighborhood": "Centre-ville",
        "latitude": 33.5928,
        "longitude": -7.6089,
        "temporal_demand": 0.69,
        "image_url": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=300&q=70",
    },
    {
        "id": 7,
        "name": "Duplex Racine",
        "property_type": "Duplex",
        "price": 960,
        "rating": 4.8,
        "neighborhood": "Racine",
        "latitude": 33.5874,
        "longitude": -7.6376,
        "temporal_demand": 0.44,
        "image_url": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=300&q=70",
    },
    {
        "id": 8,
        "name": "Studio Marina",
        "property_type": "Studio",
        "price": 580,
        "rating": 4.4,
        "neighborhood": "Marina",
        "latitude": 33.6064,
        "longitude": -7.6216,
        "temporal_demand": 0.66,
        "image_url": "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?auto=format&fit=crop&w=300&q=70",
    },
    {
        "id": 9,
        "name": "Appartement Ain Diab",
        "property_type": "Appartement entier",
        "price": 1040,
        "rating": 4.7,
        "neighborhood": "Ain Diab",
        "latitude": 33.5941,
        "longitude": -7.6709,
        "temporal_demand": 0.62,
        "image_url": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=300&q=70",
    },
    {
        "id": 10,
        "name": "Maison Californie",
        "property_type": "Villa",
        "price": 1320,
        "rating": 4.9,
        "neighborhood": "Californie",
        "latitude": 33.5663,
        "longitude": -7.6187,
        "temporal_demand": 0.36,
        "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=300&q=70",
    },
]


def seed_database(db: Session) -> None:
    if db.query(Hotel).count() > 0:
        return

    hotel_rows = []
    for item in HOTELS:
        hotel_rows.append(
            Hotel(
                province="Casablanca",
                rooms=0,
                beds=0,
                **item,
            )
        )

    airbnb_rows = []
    for item in AIRBNBS:
        airbnb_rows.append(
            Airbnb(
                property_id=f"demo_{item['id']}",
                month="2025-05",
                price_tier="midscale",
                bedrooms=1,
                revenue=0,
                stability_score=0.5,
                territorial_score=0.5,
                **item,
            )
        )

    db.add_all(hotel_rows)
    db.add_all(airbnb_rows)
    db.commit()
