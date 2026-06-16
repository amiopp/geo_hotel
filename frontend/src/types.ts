export type Hotel = {
  id: number;
  name: string;
  category: string;
  price_avg: number;
  rating: number;
  neighborhood: string;
  client_type: string;
  latitude: number;
  longitude: number;
  image_url: string;
  province?: string;
  rooms?: number;
  beds?: number;
};

export type Airbnb = {
  id: number;
  property_id?: string;
  name: string;
  property_type: string;
  price: number;
  rating: number;
  neighborhood: string;
  latitude: number;
  longitude: number;
  temporal_demand: number;
  image_url: string;
  month?: string;
  price_tier?: string;
  bedrooms?: number;
  revenue?: number;
  distance_m?: number;
  relation?: string;
};

export type Criterion = {
  label: string;
  competition_points: number;
  complementarity_points: number;
};

export type Period = {
  label: string;
  competition: number;
  complementarity: number;
};

export type HotelAnalysis = {
  hotel: Hotel;
  radius_m: number;
  airbnb_count: number;
  avg_airbnb_price: number;
  price_gap_percent: number;
  competition_score: number;
  complementarity_score: number;
  relation: string;
  criteria: Criterion[];
  periods: Period[];
  nearby_airbnbs: Airbnb[];
};
