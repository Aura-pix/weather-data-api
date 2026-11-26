# Weather Forecast API

A small FastAPI service that provides deterministic sample weather forecasts
and accepts weather alerts. It uses Python, FastAPI, Pydantic, and Uvicorn.
Forecasts are sample data for London, New York, and Tokyo, not a live weather
feed.

This repository was created to test documentation tooling and documentation
updates.

## Run locally

Use Python 3.10 or later. Install dependencies and start the development server:

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. See the [API reference](docs/api.md)
for endpoints, request and response schemas, and error behavior.
