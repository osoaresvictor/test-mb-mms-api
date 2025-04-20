# Mercado Bitcoin MMS API

This project provides a FastAPI application for calculating and retrieving Simple Moving Averages (MMS) for cryptocurrency trading pairs using historical candle data.

## 📌 Features

- RESTful API built with FastAPI
- MMS (SMA) calculation for 20, 50, and 200-day windows
- Initial and incremental data loading (via workers)
- Caching with Memcached
- Database persistence with SQLite (configurable)
- Asynchronous event simulation (Publisher/Listener)
- Monitoring script to check for missing MMS records
- Automatic infrastructure provisioning with Terraform
- CI/CD pipeline with GitHub Actions + Docker + ECS
- Organized tests (unit/integration) with pytest and Makefile
- Centralized logging (Structlog)
- Configuration via `.env`

## 🧱 Tech Stack

- **Language**: Python 3.10
- **Framework**: FastAPI
- **Cache**: Memcached
- **Database**: SQLite (for simplicity)
- **Infra**: AWS ECS Fargate + ECR + CloudWatch
- **CI/CD**: GitHub Actions
- **Infra as Code**: Terraform
- **Testing**: Pytest + unittest.mock
- **Logging**: Structlog (structured logs)

## 🔧 Setup & Run

```bash
# Lint, mypy and black
make lint

# Run full application (locally)
make run_local

# Run initial loader (locally, optional)
make initial_load

# Run incremental loader (locally, optional)
make incremental

# Run monitoring script (locally)
make monitor

# Run tests
make test-local

# Build and run with Docker
make run_in_docker
```

## 🧪 Tests

Tests are separated into:

- Unit: `tests/unit/` (e.g., services, utils, events)
- Integration: `tests/integration/` (e.g., API and DB interaction)

Run with:

```bash
pytest tests/
```

## ☁️ Cloud Deployment (Terraform + ECS)

Infrastructure is provisioned via Terraform under `/infra`. It includes:

- ECS Fargate cluster and service
- ECR for Docker image
- Security groups, IAM roles, logging
- Task Definition with environment variables
- Load Balancer (if enabled)

Update and apply:

```bash
cd infra
terraform init
terraform plan
terraform apply
```

## 📁 Project Structure

```
app/
  ├── api/              # FastAPI routes
  ├── core/             # Config, constants, logger
  ├── db/               # DB models, session and CRUD
  ├── events/           # Pub/Sub simulation
  ├── monitoring/       # Gaps check
  ├── schemas/          # Pydantic schemas
  ├── services/         # Cache + MMS logic
  ├── utils/            # MMS calculation helpers
  └── workers/          # Initial and incremental loaders
tests/
  ├── unit/
  └── integration/
```

## 🧠 Observations

- The API expects the database to be preloaded via `initial_loader.py`
- The initial loader automatically triggers the incremental loader
- Environment variables are managed via `.env`, but safely injected via Task Definition in production
- The cache TTL is configurable, but optimized for real-time coherence

---

© 2025 Victor Soares – All rights reserved.
