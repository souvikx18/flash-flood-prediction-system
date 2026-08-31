# 🌊 Flash Flood Prediction & Early Warning System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-4169E1.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-red.svg?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-orange.svg)](https://alembic.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent, data-driven **Flash Flood Prediction and Early Warning System** designed for high-risk mountainous terrains. Built with a focus on the Himalayan watershed region (**Chamoli, Uttarakhand, India**), this project integrates satellite remote sensing precipitation data, digital elevation models (DEM), and topographical geospatial features with a scalable **FastAPI** backend to provide real-time risk assessments.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
  - [Database Configuration & Migrations](#database-configuration--migrations)
  - [Running the API Server](#running-the-api-server)
- [Geospatial & ML Data Pipeline](#-geospatial--ml-data-pipeline)
- [API Documentation & Endpoints](#-api-documentation--endpoints)
- [Environment Variables](#-environment-variables)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌍 Overview

Flash floods in high-altitude Himalayan basins occur rapidly due to extreme precipitation, cloudbursts, and steep topographic gradients. This system bridges geospatial data science with production-grade web services to assess and predict flood risks:

- **Topographical Analysis**: Calculates terrain gradient and slope angles from SRTM Digital Elevation Models (DEM).
- **Precipitation Monitoring**: Collects and parses satellite rainfall data across temporal windows.
- **RESTful Inference Service**: Exposes secure API endpoints for authenticated users and monitoring stations to query real-time flood probability and risk classification (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).

---

## 🏗 System Architecture

```mermaid
flowchart TD
    subgraph Data_Pipeline["🛰️ Geospatial & ML Pipeline"]
        A[Satellite Precipitation Data] --> C[Temporal Rainfall Aggregator]
        B[SRTM Digital Elevation Model] --> D[Elevation & Slope Extractor]
        C --> E[Fused Feature Dataset]
        D --> E
        E --> F[ML Predictive Model]
    end

    subgraph Backend["⚡ FastAPI Backend Service"]
        G[Client / Mobile / Dashboard] -->|HTTP / REST| H[FastAPI Gateway]
        H --> I[JWT Auth & Security]
        H --> J[Prediction Router]
        J --> F
        H --> K[(PostgreSQL DB)]
    end
```

---

## ✨ Key Features

- **🛡️ Secure Authentication**: JWT (JSON Web Tokens) authentication with password hashing using bcrypt (`passlib`).
- **⚡ High-Performance API**: Asynchronous REST endpoints powered by **FastAPI** and **Uvicorn**.
- **🗄️ Relational Persistence & Migrations**: **SQLAlchemy 2.0** ORM coupled with **Alembic** for automated database schema tracking and migrations.
- **🗺️ Geospatial Feature Engineering**:
  - Resampling and conversion of DEM coordinates to metric gradients.
  - Calculation of slope in degrees taking into account latitude-adjusted earth curvature.
  - Spatial sampling and alignment of multi-day satellite precipitation time series.
- **📖 Interactive API Docs**: Built-in Swagger UI (`/docs`) and ReDoc (`/redoc`) specifications.

---

## 🛠 Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/), [Starlette](https://www.starlette.io/), [Uvicorn](https://www.uvicorn.org/) |
| **Database & ORM** | [PostgreSQL](https://www.postgresql.org/), [SQLAlchemy 2.0](https://www.sqlalchemy.org/), [Psycopg 3](https://www.psycopg.org/) |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) |
| **Authentication** | [Python-Jose](https://github.com/mpdavis/python-jose), [Passlib (Bcrypt)](https://passlib.readthedocs.io/) |
| **Data & Geospatial** | [Rasterio](https://rasterio.readthedocs.io/), [NumPy](https://numpy.org/), [Pandas](https://pandas.pydata.org/) |
| **Validation** | [Pydantic v2](https://docs.pydantic.dev/) |

---

## 📂 Repository Structure

```text
flash-flood-prediction-system/
├── backend/
│   ├── alembic/                 # Alembic database migration scripts & versions
│   │   ├── versions/            # Migration revisions (users, schema updates)
│   │   └── env.py               # Alembic configuration environment
│   ├── app/
│   │   ├── api/                 # API route handlers
│   │   │   ├── auth/            # Registration, login, /me routes
│   │   │   └── prediction/      # Flash flood prediction endpoints
│   │   ├── core/                # JWT verification, security & hashing utilities
│   │   ├── database/            # DB engine, session dependencies & base model
│   │   ├── models/              # SQLAlchemy ORM entities (User, etc.)
│   │   ├── schemas/             # Pydantic validation schemas
│   │   └── main.py              # FastAPI application entry point
│   ├── alembic.ini              # Alembic config file
│   └── requirements.txt         # Backend Python dependencies
├── ml/                          # Geospatial and machine learning data scripts
│   ├── create_terrain_features.py  # Computes elevation & slope from DEM raster
│   ├── download_rainfall.py        # Fetches satellite rainfall datasets
│   ├── combine_rainfall.py         # Merges multi-temporal rainfall records
│   ├── add_terrain_to_rainfall.py  # Geospatial joins of terrain + rainfall features
│   ├── merge_dem.py                # Merges multiple DEM tiles
│   └── rainfall_to_csv.py          # Converts raster precipitation to tabular CSV
├── config.py                    # Global target area configurations (Chamoli, Uttarakhand)
├── .gitignore                   # Ignored files and directories
└── README.md                    # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **PostgreSQL 14+**
- **Git**

---

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/souvikx18/flash-flood-prediction-system.git
   cd flash-flood-prediction-system
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install Backend Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r backend/requirements.txt
   ```

---

### Database Configuration & Migrations

1. **Set up your environment variables** in a `.env` file inside `backend/` or export them:
   ```env
   DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/flash_flood_db
   SECRET_KEY=your-super-secret-jwt-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

2. **Run Alembic migrations to create tables:**
   ```bash
   cd backend
   alembic upgrade head
   ```

---

### Running the API Server

Start the development server with hot reload enabled:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will now be accessible at:
- **Root Endpoint**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🛰 Geospatial & ML Data Pipeline

To extract terrain features and compile the training/inference dataset:

1. **Extract Terrain Elevation & Slope from DEM:**
   ```bash
   python ml/create_terrain_features.py
   ```
2. **Download & Process Precipitation Time Series:**
   ```bash
   python ml/download_rainfall.py
   python ml/combine_rainfall.py
   ```
3. **Fuse Terrain and Rainfall Attributes:**
   ```bash
   python ml/add_terrain_to_rainfall.py
   ```

---

## 📡 API Documentation & Endpoints

### Health Check
- `GET /health` - System health probe (`{"status": "healthy"}`)

### Authentication (`/api/auth`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/auth/register` | Register a new user account | ❌ |
| `POST` | `/api/auth/login` | Authenticate and obtain JWT Bearer token | ❌ |
| `GET` | `/api/auth/me` | Retrieve profile of the authenticated user | ✅ |

### Prediction (`/api/prediction`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/prediction/predict` | Compute flash flood probability and risk classification | ✅ |

#### Example: Prediction Request
```http
POST /api/prediction/predict HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer <YOUR_ACCESS_TOKEN>
Content-Type: application/json

{
  "latitude": 30.5524,
  "longitude": 79.5284,
  "forecast_hours": 24
}
```

#### Example: Prediction Response
```json
{
  "flood_probability": 0.12,
  "risk_level": "LOW",
  "forecast_hours": 24,
  "latitude": 30.5524,
  "longitude": 79.5284
}
```

---

## ⚙️ Environment Variables

| Variable | Type | Default / Example | Description |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | `string` | `postgresql+psycopg://user:pass@localhost:5432/dbname` | PostgreSQL connection URL |
| `SECRET_KEY` | `string` | `your_secret_key` | Secret key for signing JWT tokens |
| `ALGORITHM` | `string` | `HS256` | JWT cryptographic algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `int` | `60` | JWT token validity lifespan |

---

## 🗺️ Roadmap

- [x] Backend architecture with FastAPI & PostgreSQL.
- [x] Secure JWT authentication & user management.
- [x] Geospatial DEM processing (elevation & slope calculation).
- [x] Rainfall raster sampling and feature dataset synthesis.
- [ ] Train XGBoost / Random Forest classifier on historical flood events.
- [ ] Integrate live weather forecast APIs (e.g., Open-Meteo, IMD, ECMWF).
- [ ] Implement geospatial risk heatmaps and WebGIS dashboard with Mapbox / Leaflet.
- [ ] Real-time SMS & webhook alert dispatch system.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the project repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
