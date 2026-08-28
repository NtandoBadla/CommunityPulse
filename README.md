# CommunityPulse — Health

Live clinic crowding intelligence for community health clinics. Built for a hackathon MVP, CommunityPulse turns raw patient-flow data into a plain-language answer to the question people actually have: *"Should I go to this clinic right now, or somewhere else?"*

Health is the first vertical in a broader CommunityPulse vision — agriculture and energy are planned for later phases, once the health MVP is solid.

---

## What's working

### Backend (FastAPI + Supabase/PostgreSQL)

| Area | Status | Notes |
|---|---|---|
| Clinics database | ✅ | Name, location, coordinates, capacity, operating hours |
| Clinic metrics database | ✅ | Patients waiting/arrived/served, staff, average wait, timestamped |
| Current crowding | ✅ | Live crowding percentage from latest recorded metric |
| Crowding level | ✅ | `LOW` / `MODERATE` / `HIGH` / `CRITICAL` thresholds |
| Estimated wait time | ✅ | Derived from waiting count, served count, and average wait |
| Trend | ✅ | `INCREASING` / `DECREASING` / `STABLE`, compared against the previous metric |
| Basic forecast | ✅ | 3-hour lookahead using live arrival/service rates |
| Historical pattern analysis | ✅ | Forecast blends live trend with each clinic's hour-of-day historical average, weighted by sample size |
| Community advice | ✅ | Plain-language recommendation generated from current level + forecast |
| Nearby clinic comparison | ✅ | Haversine distance between clinics, ranked by distance then crowding |
| User accounts | ✅ | Signup/login with hashed passwords (bcrypt) and JWT bearer auth |
| Home clinic + auto-recommendation | ✅ | `/users/me/status` returns a signed-in user's home clinic status, and automatically includes nearby alternatives when that clinic is `HIGH` or `CRITICAL` |
| Alerts | ⬜ | Not yet built |

### Frontend (static HTML/CSS/JS, no build step)

| Area | Status | Notes |
|---|---|---|
| Sign up / log in | ✅ | Inline forms, JWT stored in memory for the session |
| Auth-gated dashboard | ✅ | Clinic data is only shown once signed in |
| "My clinic" panel | ✅ | Live status for the signed-in user's home clinic, with automatic alternatives when full |
| Browse-any-clinic view | ✅ | Tab through all clinics, see status, 3-hour forecast, advice, and recommendations for each |
| Visual design | ✅ | Custom "vitals monitor" theme — an animated pulse strip reflects live crowding level |

---

## Architecture

```
                  COMMUNITY PULSE
                        │
        ┌───────────────┼────────────────┐
        │               │                │
      HEALTH        AGRICULTURE       ENERGY
        │           (planned)        (planned)
     Clinics
        │
  Intelligence
        │
  Prediction + Advice
        │
  Community Action
```

```
Browser (frontend/index.html)
        │  fetch()
        ▼
FastAPI backend (localhost:8000)
        │  SQLAlchemy
        ▼
Supabase (PostgreSQL)
```

---

## Tech stack

- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
- **Database:** Supabase (PostgreSQL)
- **Auth:** JWT (`python-jose`), password hashing (`passlib` + `bcrypt`)
- **Frontend:** Plain HTML/CSS/JavaScript — no framework, no build step
- **Fonts:** IBM Plex Mono (data readouts) + IBM Plex Sans (body/UI)

---

## Project structure

```
CommunityPulse/
├── backend/
│   ├── main.py                        # App entrypoint, router registration, CORS
│   ├── database.py                    # SQLAlchemy engine/session setup
│   ├── auth.py                        # Password hashing, JWT creation/validation
│   ├── api/
│   │   ├── clinics.py                 # Clinic CRUD
│   │   ├── clinic_metrics.py          # Metrics, crowding, forecast, recommendations
│   │   ├── auth.py                    # /auth/signup, /auth/login
│   │   └── users.py                   # /users/me/status
│   ├── models/
│   │   ├── clinic.py
│   │   ├── clinic_metric.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── clinic.py
│   │   ├── clinic_metric.py
│   │   └── user.py
│   └── services/
│       ├── prediction_service.py      # Crowding, level, wait, trend, forecast, blending
│       ├── historical_service.py      # Hour-of-day historical averages
│       ├── advice_service.py          # Plain-language recommendation text
│       ├── distance_service.py        # Haversine distance between clinics
│       └── recommendation_service.py  # Shared nearby-clinic recommendation logic
├── frontend/
│   └── index.html                     # Full dashboard: auth + clinic intelligence UI
├── .env                                # DB connection string + JWT secret (not committed)
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.11+ (project has been run on 3.14)
- A Supabase project with a PostgreSQL connection string
- pip

### 1. Clone and install dependencies

```powershell
cd CommunityPulse
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy python-dotenv "passlib[bcrypt]" "bcrypt==4.0.1" python-jose "pydantic[email]"
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```
DATABASE_URL=your-supabase-postgres-connection-string
JWT_SECRET_KEY=a-long-random-string
```

Generate a secure `JWT_SECRET_KEY`:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Run the backend

```powershell
uvicorn backend.main:app --reload
```

- API base: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

On first run, all tables (`clinics`, `clinic_metrics`, `users`) are created automatically in your Supabase database.

### 4. Run the frontend

In a **second terminal**:

```powershell
cd CommunityPulse\frontend
python -m http.server 5500
```

Open `http://127.0.0.1:5500` in your browser.

> Both the backend and frontend need to be running at the same time, in separate terminals, for the dashboard to load data.

---

## Using the app

1. Open the frontend — you'll see a **sign in prompt**.
2. Click **Sign up**, choose your home clinic from the dropdown, and create an account.
3. You're automatically logged in and see:
   - **My clinic** — your home clinic's live status, with nearby alternatives shown automatically if it's busy.
   - **Browse any clinic** — tab through every clinic to see its status, 3-hour forecast, community advice, and nearby alternatives.

To seed test data, use `POST /clinics/{clinic_id}/metrics` in `/docs` to log patient counts for a clinic — the dashboard reflects new metrics immediately on refresh.

---

## API reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/clinics/` | List all clinics |
| `GET` | `/clinics/{id}` | Get a single clinic |
| `POST` | `/clinics/` | Create a clinic |
| `POST` | `/clinics/{id}/metrics` | Log a new metric snapshot for a clinic |
| `GET` | `/clinics/{id}/metrics` | List a clinic's metric history |
| `GET` | `/clinics/{id}/crowding` | Current crowding, level, wait time, trend |
| `GET` | `/clinics/{id}/forecast` | 3-hour forecast (blended with history) + advice |
| `GET` | `/clinics/{id}/recommendations` | Less-crowded nearby alternatives |
| `POST` | `/auth/signup` | Create a user account |
| `POST` | `/auth/login` | Log in, returns a JWT |
| `GET` | `/users/me/status` | Signed-in user's home clinic status + auto-recommendations |

---

## Roadmap

```
✅ Clinics database
✅ Clinic metrics database
✅ Current crowding, level, wait, trend
✅ Basic forecast
✅ Historical pattern analysis
✅ Community advice
✅ Nearby clinic comparison
✅ User accounts + home clinic
✅ Frontend dashboard
⬜ Alerts (push/notify when a clinic crosses into CRITICAL)
⬜ Agriculture MVP
⬜ Energy MVP
⬜ Unified CommunityPulse dashboard
```

---

## Notes

- The frontend keeps the auth token in memory only — refreshing the page signs you out. This was a deliberate choice for the current build; adding persistent storage (e.g. `localStorage`) is a reasonable next step if you want sessions to survive a refresh.
- `distance_km` between clinics is only computed when both clinics have latitude/longitude set. Make sure demo clinic coordinates are realistic (a few kilometers apart, not several degrees of longitude) so the numbers read believably in a demo.
