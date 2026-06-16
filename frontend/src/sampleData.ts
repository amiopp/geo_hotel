import type { Airbnb, Hotel, HotelAnalysis, Period } from "./types";

export const hotels: Hotel[] = [
  {
    id: 1,
    name: "Hôtel Atlas Center",
    category: "4 étoiles",
    price_avg: 750,
    rating: 4.3,
    neighborhood: "Centre-ville",
    client_type: "Business / Tourisme",
    latitude: 33.5899,
    longitude: -7.6214,
    image_url: "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=80",
  },
  {
    id: 2,
    name: "Hôtel Corniche Bleu",
    category: "5 étoiles",
    price_avg: 1180,
    rating: 4.6,
    neighborhood: "Ain Diab",
    client_type: "Loisir / Luxe",
    latitude: 33.5952,
    longitude: -7.6743,
    image_url: "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=900&q=80",
  },
  {
    id: 3,
    name: "Hôtel Maarif Urban",
    category: "3 étoiles",
    price_avg: 520,
    rating: 4.0,
    neighborhood: "Maarif",
    client_type: "Affaires / Court séjour",
    latitude: 33.5849,
    longitude: -7.6424,
    image_url: "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=900&q=80",
  },
  {
    id: 4,
    name: "Hôtel Casa Port",
    category: "4 étoiles",
    price_avg: 690,
    rating: 4.1,
    neighborhood: "Casa Port",
    client_type: "Business / Transit",
    latitude: 33.5991,
    longitude: -7.6135,
    image_url: "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=900&q=80",
  },
];

export const airbnbs: Airbnb[] = [
  {
    id: 1,
    name: "Appartement Gauthier",
    property_type: "Appartement entier",
    price: 650,
    rating: 4.8,
    neighborhood: "Gauthier",
    latitude: 33.5889,
    longitude: -7.6206,
    temporal_demand: 0.78,
    image_url: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=300&q=70",
  },
  {
    id: 2,
    name: "Studio Les Fleurs",
    property_type: "Studio",
    price: 520,
    rating: 4.5,
    neighborhood: "Les Fleurs",
    latitude: 33.5909,
    longitude: -7.6185,
    temporal_demand: 0.72,
    image_url: "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=300&q=70",
  },
  {
    id: 3,
    name: "Loft Maarif Central",
    property_type: "Loft",
    price: 700,
    rating: 4.7,
    neighborhood: "Maarif",
    latitude: 33.5846,
    longitude: -7.6232,
    temporal_demand: 0.58,
    image_url: "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=300&q=70",
  },
  {
    id: 4,
    name: "Suite Palmier",
    property_type: "Suite privée",
    price: 840,
    rating: 4.9,
    neighborhood: "Palmier",
    latitude: 33.5816,
    longitude: -7.6137,
    temporal_demand: 0.51,
    image_url: "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=300&q=70",
  },
  {
    id: 5,
    name: "Chambre Twin Anfa",
    property_type: "Chambre privée",
    price: 390,
    rating: 4.1,
    neighborhood: "Anfa",
    latitude: 33.5972,
    longitude: -7.6289,
    temporal_demand: 0.47,
    image_url: "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=300&q=70",
  },
  {
    id: 6,
    name: "Terrasse Centre Ville",
    property_type: "Appartement entier",
    price: 610,
    rating: 4.6,
    neighborhood: "Centre-ville",
    latitude: 33.5928,
    longitude: -7.6089,
    temporal_demand: 0.69,
    image_url: "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=300&q=70",
  },
  {
    id: 7,
    name: "Duplex Racine",
    property_type: "Duplex",
    price: 960,
    rating: 4.8,
    neighborhood: "Racine",
    latitude: 33.5874,
    longitude: -7.6376,
    temporal_demand: 0.44,
    image_url: "https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=300&q=70",
  },
  {
    id: 8,
    name: "Studio Marina",
    property_type: "Studio",
    price: 580,
    rating: 4.4,
    neighborhood: "Marina",
    latitude: 33.6064,
    longitude: -7.6216,
    temporal_demand: 0.66,
    image_url: "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?auto=format&fit=crop&w=300&q=70",
  },
  {
    id: 9,
    name: "Appartement Ain Diab",
    property_type: "Appartement entier",
    price: 1040,
    rating: 4.7,
    neighborhood: "Ain Diab",
    latitude: 33.5941,
    longitude: -7.6709,
    temporal_demand: 0.62,
    image_url: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=300&q=70",
  },
  {
    id: 10,
    name: "Maison Californie",
    property_type: "Villa",
    price: 1320,
    rating: 4.9,
    neighborhood: "Californie",
    latitude: 33.5663,
    longitude: -7.6187,
    temporal_demand: 0.36,
    image_url: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=300&q=70",
  },
];

const periods = (competition: number, complementarity: number): Period[] => [
  { label: "1 mars", competition: competition - 6, complementarity: complementarity - 4 },
  { label: "15 mars", competition: competition - 4, complementarity: complementarity - 2 },
  { label: "1 avr.", competition: competition + 7, complementarity: complementarity + 4 },
  { label: "15 avr.", competition: competition + 13, complementarity: complementarity + 6 },
  { label: "1 mai", competition: competition + 2, complementarity: complementarity - 3 },
  { label: "15 mai", competition: competition + 4, complementarity: complementarity + 1 },
].map((item) => ({
  ...item,
  competition: Math.max(0, Math.min(100, Math.round(item.competition))),
  complementarity: Math.max(0, Math.min(100, Math.round(item.complementarity))),
}));

const distanceMeters = (a: Hotel, b: Airbnb) => {
  const earthRadius = 6371000;
  const toRad = (value: number) => (value * Math.PI) / 180;
  const deltaLat = toRad(b.latitude - a.latitude);
  const deltaLon = toRad(b.longitude - a.longitude);
  const value =
    Math.sin(deltaLat / 2) ** 2 +
    Math.cos(toRad(a.latitude)) * Math.cos(toRad(b.latitude)) * Math.sin(deltaLon / 2) ** 2;
  return 2 * earthRadius * Math.asin(Math.sqrt(value));
};

const score = (value: number) => Math.max(0, Math.min(100, Math.round(value)));

export function buildFallbackAnalysis(hotelId: number, radiusM: number): HotelAnalysis {
  const hotel = hotels.find((item) => item.id === hotelId) ?? hotels[0];
  const nearby = airbnbs
    .map((item) => ({ ...item, distance_m: Math.round(distanceMeters(hotel, item)) }))
    .filter((item) => item.distance_m <= radiusM)
    .sort((a, b) => (a.distance_m ?? 0) - (b.distance_m ?? 0));

  const avgAirbnbPrice = nearby.length
    ? Math.round(nearby.reduce((sum, item) => sum + item.price, 0) / nearby.length)
    : 0;
  const priceGap = avgAirbnbPrice ? ((avgAirbnbPrice - hotel.price_avg) / hotel.price_avg) * 100 : 0;
  const avgDistance = nearby.length
    ? nearby.reduce((sum, item) => sum + (item.distance_m ?? 0), 0) / nearby.length
    : radiusM;
  const avgTemporal = nearby.length
    ? nearby.reduce((sum, item) => sum + item.temporal_demand, 0) / nearby.length
    : 0;

  const distanceCompetition = score(100 - (avgDistance / radiusM) * 55);
  const priceCompetition = score(100 - Math.min(Math.abs(priceGap), 65) * 1.25);
  const offerCompetition = hotel.client_type.includes("Business") || hotel.client_type.includes("Affaires") ? 64 : 50;
  const temporalCompetition = score(avgTemporal * 100);
  const competitionScore = score(
    distanceCompetition * 0.32 +
      priceCompetition * 0.28 +
      offerCompetition * 0.18 +
      temporalCompetition * 0.22,
  );
  const complementarityScore = score(
    (100 - distanceCompetition) * 0.22 +
      (100 - priceCompetition) * 0.24 +
      (100 - offerCompetition) * 0.24 +
      (100 - temporalCompetition) * 0.3 +
      22,
  );

  const relation =
    competitionScore >= 76
      ? "Concurrence forte"
      : competitionScore >= 58
        ? "Concurrence moyenne"
        : competitionScore >= 42
          ? "Relation mixte"
          : "Complémentarité dominante";

  const enriched = nearby.map((item) => ({
    ...item,
    relation:
      Math.abs(item.price - hotel.price_avg) <= 130 && (item.distance_m ?? radiusM) < 450
        ? "Concurrence forte"
        : (item.distance_m ?? radiusM) < radiusM * 0.65
          ? "Concurrence moyenne"
          : "Complémentarité",
  }));

  return {
    hotel,
    radius_m: radiusM,
    airbnb_count: enriched.length,
    avg_airbnb_price: avgAirbnbPrice,
    price_gap_percent: Math.round(priceGap * 10) / 10,
    competition_score: competitionScore,
    complementarity_score: complementarityScore,
    relation,
    criteria: [
      {
        label: "Distance",
        competition_points: distanceCompetition,
        complementarity_points: 100 - distanceCompetition,
      },
      {
        label: "Prix",
        competition_points: priceCompetition,
        complementarity_points: 100 - priceCompetition,
      },
      {
        label: "Type d'offre",
        competition_points: offerCompetition,
        complementarity_points: 100 - offerCompetition,
      },
      {
        label: "Temporalité",
        competition_points: temporalCompetition,
        complementarity_points: 100 - temporalCompetition,
      },
    ],
    periods: periods(competitionScore, complementarityScore),
    nearby_airbnbs: enriched,
  };
}
