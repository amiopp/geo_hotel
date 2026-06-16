# GeoHotel Insight

Géoportail web d'analyse de concurrence et de complémentarité entre hôtels et Airbnb.

## Stack

- Frontend: React, Vite, TypeScript, Leaflet, Recharts
- Backend: FastAPI, SQLAlchemy
- Base de données: PostgreSQL via Docker Compose

## Lancer l'interface

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

Si ce port est déjà pris, utilise par exemple :

```bash
cd frontend
set VITE_API_BASE_URL=http://localhost:8008&& npm run dev -- --port 5190 --strictPort
```

## Lancer l'API avec PostgreSQL

```bash
docker compose up --build
```

API: http://localhost:8000/docs

Le frontend utilise l'API si elle est disponible. Sinon, il charge les données de démonstration locales.

## Importer les vraies données PFE

Depuis la racine du projet :

```bash
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
cd backend
..\.venv\Scripts\python.exe -m app.import_data --zip "C:\Users\moham\Downloads\pfe-20260615T133749Z-3-001.zip"
```

Puis lance l'API :

```bash
cd ..
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8008
```

L'import charge 117 hôtels, 5 558 Airbnb uniques et 116 650 observations mensuelles Airbnb.
