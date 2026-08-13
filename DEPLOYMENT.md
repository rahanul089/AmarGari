# AmarGari — Setup & Deployment Guide

AmarGari (আমার গাড়ি — "My Car") is a Streamlit app backed by **Supabase
(Postgres)**. All data — users, vehicles, violations, payments, documents,
service history, notifications, appeals, activity logs — lives in your
Supabase database. There is no SQLite fallback and no local file storage;
everything reads and writes through SQLAlchemy to Postgres, so it works
the same locally and in the cloud.

---

## 1. Create your Supabase project

1. Go to https://supabase.com → **New project**.
2. Pick a name (e.g. `amargari`), a strong database password (save it
   somewhere safe — you'll need it below), and a region close to your
   users (e.g. Southeast Asia for Bangladesh).
3. Wait ~2 minutes for provisioning.

## 2. Get your connection string

1. In your Supabase project: **Project Settings → Database → Connection
   string**.
2. Select the **URI** tab, and use **Connection pooling** (transaction
   mode, port `6543`) rather than the direct connection — this is the
   one that works reliably from serverless/short-lived environments like
   Streamlit Cloud.
3. Copy the string. It looks like:
   ```
   postgresql://postgres.xxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
   ```
4. Replace `[YOUR-PASSWORD]` with your actual database password. If the
   password contains special characters (`@ : / ? #` etc.), URL-encode
   them.

You do **not** need to create any tables manually — `init_db()` runs
`SQLAlchemy`'s `create_all()` automatically on first launch, and the app
auto-seeds ~50 users / 150 vehicles / 300 violations (plus payments,
documents, service history, notifications, appeals) the first time it
finds an empty database.

## 3. Run it locally

```bash
# 1. Unzip and enter the project
cd amargari

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your database connection
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml and paste your real Supabase URI

# 5. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`. On first run it will show a
spinner ("Setting up demo data for first run…") while it creates tables
and seeds demo data — this takes 10–30 seconds depending on your
connection to Supabase.

### Demo logins (created by the seed script)

| Role  | Email                     | Password    |
|-------|---------------------------|-------------|
| Admin | `admin@amargari.gov.bd`   | `Admin@123` |
| Owner | `demo@amargari.gov.bd`    | `Demo@123`  |

You can also click **"Owner demo"** / **"Admin demo"** on the sign-in
screen instead of typing credentials. Every other seeded user has the
password `Password@123` (emails are auto-generated, visible via the
Admin → User Management tab).

### Re-seeding

The app only seeds when the `users` table is empty. To wipe and
re-generate demo data at any point:

```bash
python -m utils.seed
```

This clears all app tables (in dependency order) and regenerates fresh
mock data.

## 4. Deploy to Streamlit Community Cloud

1. Push this project to a GitHub repo (make sure `.streamlit/secrets.toml`
   is **not** committed — it's already in `.gitignore`).
2. Go to https://share.streamlit.io → **New app** → point it at your repo,
   branch `main`, main file `app.py`.
3. Before deploying, open **Advanced settings → Secrets** and paste:
   ```toml
   DATABASE_URL = "postgresql://postgres.xxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
   ```
4. Deploy. On first boot the app will create tables and seed demo data
   in your Supabase project automatically, exactly like local dev.

## 5. Deploying elsewhere (Render, Railway, Fly.io, a VPS, etc.)

Any host that can run `streamlit run app.py` works, as long as you set
the `DATABASE_URL` environment variable (the app checks Streamlit
secrets first, then falls back to `os.environ["DATABASE_URL"]`):

```bash
export DATABASE_URL="postgresql://postgres.xxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

## 6. Project structure

```
amargari/
├── app.py                     # Landing page, sign in / register, home dashboard entry
├── requirements.txt
├── DEPLOYMENT.md
├── .gitignore
├── .streamlit/
│   ├── config.toml            # Native Streamlit theme (matches brand blue)
│   └── secrets.toml.example   # Copy to secrets.toml and fill in DATABASE_URL
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Vehicles.py
│   ├── 3_Violations.py
│   ├── 4_Payments.py
│   ├── 5_Documents.py
│   ├── 6_Service_History.py
│   ├── 7_Notifications.py
│   ├── 8_Appeals.py
│   ├── 9_Admin.py             # admin-only: users, appeals review, activity log, settings
│   ├── 10_Reports.py          # CSV / PDF export
│   ├── 11_Analytics.py        # charts (plotly)
│   ├── 12_Mock_BRTA_API.py    # simulated gov. API lookups (demo only)
│   └── 13_AI_Demo.py          # simulated image "violation detection" (demo only)
├── utils/
│   ├── db.py                  # SQLAlchemy models + Supabase session (all persistent data)
│   ├── auth.py                 # bcrypt password hashing + session-based login/RBAC
│   ├── pdf_utils.py            # ReportLab receipt/report generation
│   └── seed.py                 # Mock Bangladesh-flavored data generator
└── styles/
    ├── theme.py                # CSS variables, light/dark mode, brand styling
    └── components.py           # page_header, badge, metric_card, stat, vehicle_card
```

## 7. Notes on scale

This schema comfortably handles far more than the seeded demo volume —
Supabase's free tier gives you 500MB of Postgres storage and pooled
connections, which is enough for tens of thousands of violations/vehicles.
If you outgrow it, the only change needed is upgrading your Supabase plan;
no application code changes are required since everything already goes
through the pooled connection with `pool_pre_ping` and `pool_recycle` set
for long-lived managed Postgres.

## 8. Security notes before going further than a demo

- Change the seeded demo/admin passwords (or delete those accounts) before
  using this with real users.
- Rotate your Supabase database password if it was ever pasted anywhere
  public.
- The "Mock BRTA API" and "AI Demo" pages are explicitly simulated/demo
  features (clearly labeled in-app) — they do not call any real
  government system or computer-vision model.
- Add row-level security policies in Supabase if you ever expose the
  Postgres connection to more than this single trusted app server.
