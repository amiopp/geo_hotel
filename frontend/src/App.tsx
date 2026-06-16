import { useEffect, useMemo, useState, type FormEvent } from "react";
import L from "leaflet";
import { Circle, CircleMarker, MapContainer, Marker, TileLayer, Tooltip, useMap, ZoomControl } from "react-leaflet";
import {
  ArrowRight,
  BarChart3,
  Bell,
  Building2,
  CalendarDays,
  ChevronDown,
  CircleDollarSign,
  Clock3,
  Eye,
  EyeOff,
  Home,
  Info,
  Layers3,
  ListFilter,
  LockKeyhole,
  LogOut,
  Map as MapIcon,
  MapPin,
  Navigation,
  Puzzle,
  Search,
  ShieldAlert,
  ShieldCheck,
  Star,
  TrendingDown,
  UserRound,
  UsersRound,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip as ChartTooltip,
  XAxis,
  YAxis,
} from "recharts";
import { fetchAnalysis, fetchHotels, loginUser } from "./api";
import { buildFallbackAnalysis } from "./sampleData";
import type { Airbnb, Criterion, Hotel, HotelAnalysis } from "./types";

const radii = [500, 1000, 2000, 5000];
const DEFAULT_HOTEL_ID = 89;
const AUTH_STORAGE_KEY = "geohotel_auth_session";
const HOTEL_IMAGE_FALLBACK =
  "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=80";

const tabs = [
  { id: "overview", label: "Vue générale", icon: BarChart3 },
  { id: "competition", label: "Concurrence", icon: ShieldAlert },
  { id: "complementarity", label: "Complémentarité", icon: Puzzle },
  { id: "time", label: "Analyse temporelle", icon: Clock3 },
  { id: "airbnb", label: "Détails Airbnb", icon: ListFilter },
] as const;

type TabId = (typeof tabs)[number]["id"];

type AuthSession = {
  token: string;
  userName: string;
  identifier: string;
};

function readAuthSession(): AuthSession | null {
  const raw = localStorage.getItem(AUTH_STORAGE_KEY) ?? sessionStorage.getItem(AUTH_STORAGE_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as AuthSession;
  } catch {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    sessionStorage.removeItem(AUTH_STORAGE_KEY);
    return null;
  }
}

function saveAuthSession(session: AuthSession, remember: boolean) {
  localStorage.removeItem(AUTH_STORAGE_KEY);
  sessionStorage.removeItem(AUTH_STORAGE_KEY);
  const storage = remember ? localStorage : sessionStorage;
  storage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
}

function clearAuthSession() {
  localStorage.removeItem(AUTH_STORAGE_KEY);
  sessionStorage.removeItem(AUTH_STORAGE_KEY);
}

function formatDh(value: number) {
  return `${Math.round(value).toLocaleString("fr-FR")} DH`;
}

function formatRadius(radius: number) {
  return radius >= 1000 ? `${radius / 1000} km` : `${radius} m`;
}

function markerIcon(kind: "hotel" | "airbnb", selected = false) {
  const size = selected ? 48 : 36;
  return L.divIcon({
    html: `<div class="geo-pin geo-pin--${kind} ${selected ? "geo-pin--selected" : ""}"><span>${
      kind === "hotel" ? "H" : "A"
    }</span></div>`,
    className: "geo-pin-host",
    iconSize: [size, size],
    iconAnchor: [size / 2, size - 3],
  });
}

function FlyToSelected({ center, radius }: { center: [number, number]; radius: number }) {
  const map = useMap();

  useEffect(() => {
    const circleBounds = L.latLng(center).toBounds(radius * 2);
    map.flyToBounds(circleBounds, {
      duration: 0.6,
      padding: [42, 42],
      maxZoom: radius >= 5000 ? 12 : radius >= 2000 ? 13 : 15,
    });
  }, [center, map, radius]);

  return null;
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: "orange" | "green" | "blue" }) {
  return (
    <div className="score-line">
      <div className="score-line__top">
        <span>{label}</span>
        <strong>{value} / 100</strong>
      </div>
      <div className="score-track">
        <span className={`score-fill score-fill--${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function RelationBadge({ relation }: { relation: string }) {
  const tone = relation.includes("forte")
    ? "danger"
    : relation.includes("Complémentarité")
      ? "success"
      : "warning";
  return <span className={`relation-badge relation-badge--${tone}`}>{relation}</span>;
}

function CriterionCard({ criterion }: { criterion: Criterion }) {
  const finalScore = Math.round((criterion.competition_points + (100 - criterion.complementarity_points)) / 2);

  return (
    <article className="criterion-card">
      <div>
        <p>{criterion.label}</p>
        <strong>{finalScore} pts</strong>
      </div>
      <ScoreBar label="Concurrence" value={criterion.competition_points} color="orange" />
      <ScoreBar label="Complémentarité" value={criterion.complementarity_points} color="green" />
    </article>
  );
}

function AirbnbRows({ airbnbs, compact = false }: { airbnbs: Airbnb[]; compact?: boolean }) {
  const visibleRows = compact ? airbnbs.slice(0, 3) : airbnbs;

  return (
    <div className="table-wrap">
      <table className="airbnb-table">
        <thead>
          <tr>
            <th>Nom</th>
            <th>Distance</th>
            <th>Prix</th>
            <th>Note</th>
            <th>Relation</th>
          </tr>
        </thead>
        <tbody>
          {visibleRows.map((airbnb) => (
            <tr key={airbnb.id}>
              <td>
                <div className="table-name">
                  <img src={airbnb.image_url} alt="" />
                  <span>
                    <strong>{airbnb.name}</strong>
                    <small>{airbnb.property_type}</small>
                  </span>
                </div>
              </td>
              <td>{airbnb.distance_m ? `${airbnb.distance_m} m` : "-"}</td>
              <td>{formatDh(airbnb.price)}</td>
              <td>{airbnb.rating.toFixed(1)}</td>
              <td>
                <RelationBadge relation={airbnb.relation ?? "Relation mixte"} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function OverviewTab({ analysis }: { analysis: HotelAnalysis }) {
  const radarData = analysis.criteria.map((item) => ({
    label: item.label === "Type d'offre" ? "Offre" : item.label,
    concurrence: item.competition_points,
    complementarite: item.complementarity_points,
  }));

  return (
    <div className="overview-grid">
      <section className="panel-block">
        <div className="block-heading">
          <h3>Synthèse des critères</h3>
          <span>Score final {analysis.competition_score}/100</span>
        </div>
        <div className="radar-box">
          <ResponsiveContainer width="100%" height={250}>
            <RadarChart data={radarData} outerRadius={88}>
              <PolarGrid />
              <PolarAngleAxis dataKey="label" tick={{ fill: "#52627a", fontSize: 12 }} />
              <Radar dataKey="concurrence" stroke="#1f77e8" fill="#1f77e8" fillOpacity={0.25} />
              <Radar dataKey="complementarite" stroke="#1fa463" fill="#1fa463" fillOpacity={0.12} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="panel-block">
        <div className="block-heading">
          <h3>Évolution par période</h3>
          <span>Données mensuelles</span>
        </div>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={analysis.periods} margin={{ top: 12, right: 16, left: -18, bottom: 0 }}>
            <CartesianGrid stroke="#edf1f7" vertical={false} />
            <XAxis dataKey="label" tick={{ fill: "#66758a", fontSize: 11 }} tickLine={false} />
            <YAxis domain={[0, 100]} tick={{ fill: "#66758a", fontSize: 11 }} tickLine={false} />
            <ChartTooltip />
            <Line type="monotone" dataKey="competition" stroke="#1f77e8" strokeWidth={3} dot={{ r: 4 }} />
            <Line type="monotone" dataKey="complementarity" stroke="#1fa463" strokeWidth={3} dot={{ r: 4 }} />
          </LineChart>
        </ResponsiveContainer>
      </section>

      <section className="panel-block panel-block--table">
        <div className="block-heading">
          <h3>Airbnb à proximité</h3>
          <span>Top 3</span>
        </div>
        <AirbnbRows airbnbs={analysis.nearby_airbnbs} compact />
      </section>
    </div>
  );
}

function CompetitionTab({ analysis }: { analysis: HotelAnalysis }) {
  const data = analysis.criteria.map((item) => ({
    name: item.label,
    score: item.competition_points,
  }));

  return (
    <div className="tab-two-col">
      <section className="panel-block">
        <div className="block-heading">
          <h3>Intensité concurrentielle</h3>
          <span>{analysis.relation}</span>
        </div>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={data} margin={{ top: 12, right: 12, left: -20, bottom: 0 }}>
            <CartesianGrid stroke="#edf1f7" vertical={false} />
            <XAxis dataKey="name" tick={{ fill: "#66758a", fontSize: 11 }} tickLine={false} />
            <YAxis domain={[0, 100]} tick={{ fill: "#66758a", fontSize: 11 }} tickLine={false} />
            <ChartTooltip />
            <Bar dataKey="score" radius={[6, 6, 0, 0]}>
              {data.map((_, index) => (
                <Cell key={index} fill={index === 1 ? "#ff6b1a" : "#1f77e8"} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </section>
      <section className="panel-block insight-list">
        <div className="block-heading">
          <h3>Signaux clés</h3>
          <span>{analysis.airbnb_count} annonces</span>
        </div>
        <article>
          <ShieldAlert size={18} />
          <div>
            <strong>Prix substituable</strong>
            <p>L'écart moyen est de {analysis.price_gap_percent.toFixed(1)} %, ce qui rapproche l'offre hôtelière des locations courtes durées.</p>
          </div>
        </article>
        <article>
          <MapPin size={18} />
          <div>
            <strong>Proximité élevée</strong>
            <p>Les annonces les plus proches sont situées dans le buffer de {formatRadius(analysis.radius_m)} autour de l'hôtel.</p>
          </div>
        </article>
        <article>
          <UsersRound size={18} />
          <div>
            <strong>Clientèle recoupée</strong>
            <p>Le profil business et tourisme renforce le risque de substitution en semaine.</p>
          </div>
        </article>
      </section>
    </div>
  );
}

function ComplementarityTab({ analysis }: { analysis: HotelAnalysis }) {
  const complementarityRows = analysis.criteria.map((item) => ({
    label: item.label,
    value: item.complementarity_points,
  }));

  return (
    <div className="tab-two-col">
      <section className="panel-block opportunity-panel">
        <div className="block-heading">
          <h3>Potentiel de complémentarité</h3>
          <span>{analysis.complementarity_score}/100</span>
        </div>
        {complementarityRows.map((item) => (
          <ScoreBar key={item.label} label={item.label} value={item.value} color="green" />
        ))}
      </section>
      <section className="panel-block insight-list">
        <div className="block-heading">
          <h3>Opportunités</h3>
          <span>Segmentation</span>
        </div>
        <article>
          <Puzzle size={18} />
          <div>
            <strong>Séjours longs</strong>
            <p>Les appartements peuvent absorber une demande familiale ou longue durée sans cannibaliser les nuitées business.</p>
          </div>
        </article>
        <article>
          <Home size={18} />
          <div>
            <strong>Offre élargie</strong>
            <p>Les typologies loft et villa complètent les chambres standard dans les quartiers périphériques.</p>
          </div>
        </article>
        <article>
          <CalendarDays size={18} />
          <div>
            <strong>Périodes creuses</strong>
            <p>La complémentarité augmente quand la demande hôtelière ralentit hors événements professionnels.</p>
          </div>
        </article>
      </section>
    </div>
  );
}

function TimeTab({ analysis }: { analysis: HotelAnalysis }) {
  return (
    <section className="panel-block full-width-block">
      <div className="block-heading">
        <h3>Analyse temporelle</h3>
        <span>Derniers mois disponibles</span>
      </div>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={analysis.periods} margin={{ top: 16, right: 22, left: -12, bottom: 4 }}>
          <CartesianGrid stroke="#edf1f7" vertical={false} />
          <XAxis dataKey="label" tick={{ fill: "#66758a", fontSize: 12 }} tickLine={false} />
          <YAxis domain={[0, 100]} tick={{ fill: "#66758a", fontSize: 12 }} tickLine={false} />
          <ChartTooltip />
          <Line type="monotone" dataKey="competition" name="Concurrence" stroke="#ff6b1a" strokeWidth={3} dot={{ r: 5 }} />
          <Line
            type="monotone"
            dataKey="complementarity"
            name="Complémentarité"
            stroke="#1fa463"
            strokeWidth={3}
            dot={{ r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
      <div className="temporal-notes">
        <span>Score calculé par mois</span>
        <span>Prix, occupation et densité</span>
        <span>Période réelle Airbnb</span>
      </div>
    </section>
  );
}

function AirbnbTab({ analysis }: { analysis: HotelAnalysis }) {
  return (
    <section className="panel-block full-width-block">
      <div className="block-heading">
        <h3>Détails Airbnb proches</h3>
        <span>
          {analysis.airbnb_count} annonces dans le buffer
          {analysis.nearby_airbnbs.length < analysis.airbnb_count
            ? `, ${analysis.nearby_airbnbs.length} affichées`
            : ""}
        </span>
      </div>
      <AirbnbRows airbnbs={analysis.nearby_airbnbs} />
    </section>
  );
}

function ActiveTabContent({ tab, analysis }: { tab: TabId; analysis: HotelAnalysis }) {
  if (tab === "competition") return <CompetitionTab analysis={analysis} />;
  if (tab === "complementarity") return <ComplementarityTab analysis={analysis} />;
  if (tab === "time") return <TimeTab analysis={analysis} />;
  if (tab === "airbnb") return <AirbnbTab analysis={analysis} />;
  return <OverviewTab analysis={analysis} />;
}

function LoginScreen({ onLogin }: { onLogin: (session: AuthSession, remember: boolean) => void }) {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const mapTiles = [
    "https://tile.openstreetmap.org/13/3921/3282.png",
    "https://tile.openstreetmap.org/13/3922/3282.png",
    "https://tile.openstreetmap.org/13/3923/3282.png",
    "https://tile.openstreetmap.org/13/3921/3283.png",
    "https://tile.openstreetmap.org/13/3922/3283.png",
    "https://tile.openstreetmap.org/13/3923/3283.png",
    "https://tile.openstreetmap.org/13/3921/3284.png",
    "https://tile.openstreetmap.org/13/3922/3284.png",
    "https://tile.openstreetmap.org/13/3923/3284.png",
  ];

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    if (!identifier.trim() || !password) {
      setError("Veuillez saisir l'identifiant et le mot de passe.");
      return;
    }

    setLoading(true);
    try {
      const response = await loginUser(identifier.trim(), password);
      onLogin(
        {
          token: response.access_token,
          userName: response.user_name,
          identifier: identifier.trim(),
        },
        remember,
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Connexion impossible pour le moment.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="login-shell">
      <section className="login-brand-panel" aria-label="Présentation GeoHotel Insight">
        <div className="login-brand-lockup">
          <img src="/geohotel-logo-mark.png" alt="" />
          <div>
            <strong>
              Geo<span>Hotel</span>
            </strong>
            <small>Insight</small>
          </div>
        </div>

        <div className="login-copy">
          <h1>
            Analysez la relation entre <span>hôtels</span> et <em>Airbnb</em> pour de meilleures décisions
          </h1>
          <i />
        </div>

        <div className="login-feature-list">
          <span>
            <MapIcon size={21} />
            Carte interactive
          </span>
          <span>
            <UsersRound size={21} />
            Analyse de concurrence
          </span>
          <span>
            <Puzzle size={21} />
            Complémentarité
          </span>
          <span>
            <Clock3 size={21} />
            Analyse temporelle
          </span>
          <span>
            <ShieldCheck size={21} />
            Données sécurisées
          </span>
        </div>

        <div className="login-visual" aria-hidden="true">
          <span className="login-buffer-ring login-buffer-ring--outer" />
          <span className="login-buffer-ring login-buffer-ring--inner" />
          <span className="login-mini-pin login-mini-pin--one"><b>A</b></span>
          <span className="login-mini-pin login-mini-pin--two"><b>A</b></span>
          <span className="login-mini-pin login-mini-pin--three"><b>A</b></span>
          <div className="login-building">
            <Building2 size={58} />
            <small>HOTEL</small>
          </div>
        </div>
      </section>

      <section className="login-map-panel">
        <div className="login-map-tiles" aria-hidden="true">
          {mapTiles.map((tile) => (
            <img key={tile} src={tile} alt="" />
          ))}
        </div>
        <div className="login-map-wash" />
        <span className="login-map-pin login-map-pin--hotel login-map-pin--top"><b>H</b></span>
        <span className="login-map-pin login-map-pin--hotel login-map-pin--left"><b>H</b></span>
        <span className="login-map-pin login-map-pin--airbnb login-map-pin--mid"><b>A</b></span>
        <span className="login-map-pin login-map-pin--airbnb login-map-pin--low"><b>A</b></span>

        <form className="login-card" onSubmit={handleSubmit}>
          <div className="login-card-heading">
            <p>Bienvenue sur</p>
            <h2>
              GeoHotel <span>Insight</span>
            </h2>
            <small>Connectez-vous à votre espace d'analyse</small>
          </div>

          <div className="login-mode">Connexion sécurisée</div>

          <label className="login-field">
            <UserRound size={22} />
            <input
              value={identifier}
              onChange={(event) => setIdentifier(event.target.value)}
              placeholder="Identifiant"
              autoComplete="username"
            />
          </label>

          <label className="login-field">
            <LockKeyhole size={22} />
            <input
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Mot de passe"
              type={showPassword ? "text" : "password"}
              autoComplete="current-password"
            />
            <button
              className="login-eye"
              type="button"
              aria-label={showPassword ? "Masquer le mot de passe" : "Afficher le mot de passe"}
              onClick={() => setShowPassword((value) => !value)}
            >
              {showPassword ? <EyeOff size={21} /> : <Eye size={21} />}
            </button>
          </label>

          <div className="login-options">
            <label>
              <input
                checked={remember}
                type="checkbox"
                onChange={(event) => setRemember(event.target.checked)}
              />
              <span>Se souvenir de moi</span>
            </label>
            <strong>Utilisateur unique</strong>
          </div>

          {error && (
            <p className="login-error" role="alert" aria-live="polite">
              {error}
            </p>
          )}

          <button className="login-submit" type="submit" disabled={loading}>
            <span>{loading ? "Connexion..." : "Se connecter"}</span>
            {loading ? <Navigation size={21} /> : <ArrowRight size={23} />}
          </button>

          <div className="login-secure-note">
            <ShieldCheck size={20} />
            Vos données d'analyse restent protégées
          </div>
        </form>

        <span className="login-attribution">© OpenStreetMap</span>
      </section>
    </main>
  );
}

export default function App() {
  const [authSession, setAuthSession] = useState<AuthSession | null>(() => readAuthSession());
  const [hotels, setHotels] = useState<Hotel[]>([]);
  const [selectedHotelId, setSelectedHotelId] = useState(DEFAULT_HOTEL_ID);
  const [radius, setRadius] = useState(1000);
  const [activeTab, setActiveTab] = useState<TabId>("overview");
  const [query, setQuery] = useState("");
  const [startDate, setStartDate] = useState("2025-05-15");
  const [endDate, setEndDate] = useState("2025-05-22");
  const [analysis, setAnalysis] = useState<HotelAnalysis>(() => buildFallbackAnalysis(DEFAULT_HOTEL_ID, 1000));

  useEffect(() => {
    if (!authSession) return;
    let cancelled = false;
    fetchHotels(authSession.token).then((items) => {
      if (cancelled) return;
      setHotels(items);
      setSelectedHotelId((currentId) => (items.length && !items.some((item) => item.id === currentId) ? items[0].id : currentId));
    });
    return () => {
      cancelled = true;
    };
  }, [authSession]);

  useEffect(() => {
    if (!authSession) return;
    let cancelled = false;
    fetchAnalysis(selectedHotelId, radius, authSession.token).then((nextAnalysis) => {
      if (!cancelled) {
        setAnalysis(nextAnalysis);
      }
    });
    return () => {
      cancelled = true;
    };
  }, [authSession, selectedHotelId, radius]);

  function handleLogin(session: AuthSession, remember: boolean) {
    saveAuthSession(session, remember);
    setAuthSession(session);
  }

  const filteredHotels = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) return hotels;
    return hotels.filter((hotel) => hotel.name.toLowerCase().includes(normalized));
  }, [hotels, query]);

  function handleLogout() {
    clearAuthSession();
    setAuthSession(null);
    setQuery("");
  }

  function handleStartDateChange(value: string) {
    setStartDate(value);
    if (value > endDate) {
      setEndDate(value);
    }
  }

  function handleEndDateChange(value: string) {
    setEndDate(value < startDate ? startDate : value);
  }

  if (!authSession) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  const selectedHotel = analysis.hotel;
  const center: [number, number] = [selectedHotel.latitude, selectedHotel.longitude];
  const mapAirbnbs = analysis.nearby_airbnbs;
  const showAirbnbTooltips = mapAirbnbs.length <= 1200;

  const relationIcon = analysis.relation.includes("Complémentarité") ? Puzzle : UsersRound;
  const RelationIcon = relationIcon;
  const gapTone = analysis.price_gap_percent <= 0 ? "positive" : "negative";
  const userInitials =
    authSession.userName
      .split(" ")
      .filter(Boolean)
      .map((part) => part[0])
      .join("")
      .slice(0, 2)
      .toUpperCase() || "GH";

  return (
    <div className="app-shell">
      <header className="topbar topbar--simple">
        <div className="brand">
          <img className="brand-logo" src="/geohotel-logo.png" alt="GeoHotel Insight" />
        </div>

        <label className="date-filter date-filter--range">
          <span>Date</span>
          <div className="date-range-control">
            <CalendarDays size={18} />
            <input
              aria-label="Date de début"
              type="date"
              value={startDate}
              onChange={(event) => handleStartDateChange(event.target.value)}
            />
            <span className="date-range-separator">-</span>
            <input
              aria-label="Date de fin"
              type="date"
              value={endDate}
              min={startDate}
              onChange={(event) => handleEndDateChange(event.target.value)}
            />
          </div>
        </label>

        <button className="simple-logout" type="button" onClick={handleLogout}>
          <LogOut size={18} />
          <span>Déconnexion</span>
        </button>

        <div className="filters">
          <label>
            <span>Ville</span>
            <select defaultValue="Casablanca">
              <option>Casablanca</option>
              <option>Rabat</option>
              <option>Marrakech</option>
            </select>
            <ChevronDown size={15} />
          </label>
          <label className="date-filter">
            <span>Date</span>
            <CalendarDays size={16} />
            <select defaultValue="15 mai - 22 mai 2025">
              <option>15 mai - 22 mai 2025</option>
              <option>1 juin - 8 juin 2025</option>
              <option>15 juin - 22 juin 2025</option>
            </select>
            <ChevronDown size={15} />
          </label>
          <label>
            <span>Saison</span>
            <select defaultValue="Printemps">
              <option>Printemps</option>
              <option>Été</option>
              <option>Automne</option>
              <option>Hiver</option>
            </select>
            <ChevronDown size={15} />
          </label>
          <label>
            <span>Catégorie hôtel</span>
            <select defaultValue="4 étoiles">
              <option>4 étoiles</option>
              <option>3 étoiles</option>
              <option>5 étoiles</option>
            </select>
            <ChevronDown size={15} />
          </label>
        </div>

        <div className="top-actions">
          <div className="search-box">
            <Search size={18} />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Rechercher un hôtel"
              list="hotel-options"
            />
            <datalist id="hotel-options">
              {filteredHotels.map((hotel) => (
                <option key={hotel.id} value={hotel.name} />
              ))}
            </datalist>
            {query && (
              <button
                type="button"
                onClick={() => {
                  const match = hotels.find((hotel) => hotel.name.toLowerCase() === query.trim().toLowerCase());
                  if (match) setSelectedHotelId(match.id);
                }}
              >
                <Search size={16} />
              </button>
            )}
          </div>
          <button className="icon-button" type="button" aria-label="Notifications">
            <Bell size={20} />
          </button>
          <button className="logout-button" type="button" onClick={handleLogout}>
            <LogOut size={18} />
            <span>Déconnexion</span>
          </button>
          <button className="avatar" type="button" aria-label={authSession.userName}>{userInitials}</button>
        </div>
      </header>

      <main className="workspace">
        <section className="map-panel">
          <MapContainer center={center} zoom={14} zoomControl={false} preferCanvas className="map-canvas">
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <ZoomControl position="topleft" />
            <FlyToSelected center={center} radius={radius} />
            <Circle
              center={center}
              radius={radius}
              pathOptions={{ color: "#1f77e8", fillColor: "#1f77e8", fillOpacity: 0.14, weight: 2, dashArray: "8 8" }}
            />
            {mapAirbnbs.map((airbnb) => (
              <CircleMarker
                key={airbnb.id}
                center={[airbnb.latitude, airbnb.longitude]}
                radius={5}
                pathOptions={{ color: "#ffffff", fillColor: "#ff6b1a", fillOpacity: 0.9, weight: 1.5 }}
              >
                {showAirbnbTooltips && (
                  <Tooltip direction="top" offset={[0, -18]}>
                    {airbnb.name} - {formatDh(airbnb.price)}
                  </Tooltip>
                )}
              </CircleMarker>
            ))}
            {hotels.map((hotel) => (
              <Marker
                key={hotel.id}
                position={[hotel.latitude, hotel.longitude]}
                icon={markerIcon("hotel", hotel.id === selectedHotelId)}
                eventHandlers={{ click: () => setSelectedHotelId(hotel.id) }}
              >
                <Tooltip
                  direction="right"
                  offset={[18, -16]}
                  permanent={hotel.id === selectedHotelId}
                  className="hotel-tooltip"
                >
                  {hotel.name}
                </Tooltip>
              </Marker>
            ))}
          </MapContainer>

          <div className="radius-control map-floating">
            {radii.map((item) => (
              <button
                key={item}
                type="button"
                className={item === radius ? "active" : ""}
                onClick={() => setRadius(item)}
              >
                {formatRadius(item)}
              </button>
            ))}
          </div>

          <div className="legend map-floating">
            <span><i className="legend-dot legend-dot--hotel" />Hôtel</span>
            <span><i className="legend-dot legend-dot--airbnb" />Airbnb</span>
            <span><i className="legend-ring" />Buffer ({formatRadius(radius)})</span>
          </div>

          <button className="map-info map-floating" type="button" aria-label="Information carte">
            <Info size={22} />
          </button>
        </section>

        <aside className="dashboard">
          <section className="hotel-summary">
            <img
              src={selectedHotel.image_url}
              alt=""
              referrerPolicy="no-referrer"
              onError={(event) => {
                event.currentTarget.onerror = null;
                event.currentTarget.src = HOTEL_IMAGE_FALLBACK;
              }}
            />
            <div className="hotel-main">
              <h1>{selectedHotel.name}</h1>
              <div className="stars" aria-label={`Note ${selectedHotel.rating}/5`}>
                {[1, 2, 3, 4, 5].map((item) => (
                  <Star key={item} size={18} fill={item <= Math.round(selectedHotel.rating) ? "#f7b500" : "transparent"} />
                ))}
              </div>
              <p>Prix moyen : <strong>{formatDh(selectedHotel.price_avg)} / nuit</strong></p>
              <p>Note : <strong>{selectedHotel.rating.toFixed(1)} / 5</strong></p>
              <p>Quartier : <strong>{selectedHotel.neighborhood}</strong></p>
              <p>Type : <strong>{selectedHotel.client_type}</strong></p>
            </div>
            <div className="buffer-card">
              <div>
                <strong>Buffer d'analyse</strong>
                <Info size={16} />
              </div>
              <div className="buffer-buttons">
                {radii.map((item) => (
                  <button
                    key={item}
                    type="button"
                    className={item === radius ? "active" : ""}
                    onClick={() => setRadius(item)}
                  >
                    {formatRadius(item)}
                  </button>
                ))}
              </div>
            </div>
          </section>

          <section className="stats-grid">
            <article className="stat-card">
              <span>
                <Home size={24} />
              </span>
              <p>Airbnb détectés</p>
              <strong>{analysis.airbnb_count}</strong>
            </article>
            <article className="stat-card">
              <span>
                <CircleDollarSign size={24} />
              </span>
              <p>Prix moyen Airbnb</p>
              <strong>{formatDh(analysis.avg_airbnb_price)}</strong>
            </article>
            <article className={`stat-card stat-card--${gapTone}`}>
              <span>
                <TrendingDown size={24} />
              </span>
              <p>Écart prix</p>
              <strong>{analysis.price_gap_percent > 0 ? "+" : ""}{analysis.price_gap_percent.toFixed(1)} %</strong>
            </article>
          </section>

          <section className="relation-panel">
            <div className="dominant-relation">
              <span>
                <RelationIcon size={30} />
              </span>
              <div>
                <p>Relation dominante</p>
                <strong>{analysis.relation}</strong>
              </div>
            </div>
            <div className="relation-scores">
              <ScoreBar label="Score concurrence" value={analysis.competition_score} color="orange" />
              <ScoreBar label="Score complémentarité" value={analysis.complementarity_score} color="green" />
            </div>
          </section>

          <section className="criteria-strip">
            <div className="criteria-title">
              <Layers3 size={18} />
              <strong>Critères de calcul</strong>
              <span>Score final {analysis.competition_score}/100</span>
            </div>
            <div className="criteria-grid">
              {analysis.criteria.map((criterion) => (
                <CriterionCard key={criterion.label} criterion={criterion} />
              ))}
            </div>
          </section>

          <section className="tabs-panel">
            <nav className="tabs" aria-label="Analyses">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    type="button"
                  className={activeTab === tab.id ? "active" : ""}
                  onClick={() => setActiveTab(tab.id)}
                >
                  <Icon size={18} />
                  <span>{tab.label}</span>
                </button>
              );
            })}
            </nav>
            <div className="tab-content">
              <ActiveTabContent tab={activeTab} analysis={analysis} />
            </div>
          </section>
        </aside>
      </main>
    </div>
  );
}
