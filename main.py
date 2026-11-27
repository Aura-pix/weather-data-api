from datetime import datetime, timezone
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

app = FastAPI(
    title="Weather Forecast API",
    description="A small API serving deterministic sample weather forecasts and alerts.",
    version="1.0.0",
)


class WeatherResponse(BaseModel):
    temperature: float
    humidity: int
    condition: str
    timestamp: datetime


class WeatherAlertRequest(BaseModel):
    severity: str
    message: str


_FORECASTS = {
    "london": WeatherResponse(
        temperature=12.5,
        humidity=78,
        condition="Cloudy",
        timestamp=datetime(2026, 11, 25, tzinfo=timezone.utc),
    ),
    "new york": WeatherResponse(
        temperature=8.0,
        humidity=64,
        condition="Partly cloudy",
        timestamp=datetime(2026, 11, 25, tzinfo=timezone.utc),
    ),
    "tokyo": WeatherResponse(
        temperature=16.2,
        humidity=58,
        condition="Clear",
        timestamp=datetime(2026, 11, 25, tzinfo=timezone.utc),
    ),
}

_bearer_auth = HTTPBearer(auto_error=False)


@app.get("/cities", response_model=list[str])
def get_cities() -> list[str]:
    return list(_FORECASTS)


@app.get(
    "/weather/{city}",
    response_model=WeatherResponse,
    responses={404: {"description": "Unknown city"}},
)
def get_weather(
    city: str,
    unit: Annotated[Literal["C", "F", "K"], Query()] = "C",  # ADDED "K"
    include_wind: Annotated[bool, Query(description="Include wind speed")] = False, # NEW PARAM
) -> WeatherResponse:
    forecast = _FORECASTS.get(city.strip().casefold())
    if forecast is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No forecast available for city '{city}'.",
        )

    if unit == "F":
        return forecast.model_copy(
            update={"temperature": round(forecast.temperature * 9 / 5 + 32, 1)}
        )
    elif unit == "K": # NEW KELVIN LOGIC
        return forecast.model_copy(
            update={"temperature": round(forecast.temperature + 273.15, 2)}
        )
        
    return forecast


@app.post(
    "/weather/alerts",
    response_model=WeatherAlertRequest,
    status_code=status.HTTP_201_CREATED,
    responses={401: {"description": "Missing or invalid bearer token"}},
)
def create_weather_alert(
    alert: WeatherAlertRequest,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(_bearer_auth)
    ],
) -> WeatherAlertRequest:
    if credentials is None or not credentials.credentials.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A bearer token is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return alert

@app.delete(
    "/weather/alerts/{alert_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={403: {"description": "Forbidden"}},
)
def delete_weather_alert(alert_id: int) -> None:
    if alert_id == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete the primary alert.",
        )
    return None