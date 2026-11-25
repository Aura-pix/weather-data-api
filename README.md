# Weather Forecast API

A small FastAPI service that returns deterministic sample forecasts and accepts
authenticated weather alerts. Forecast data is provided for London, New York,
and Tokyo; it is sample data, not a live weather feed.

## Run locally

Use Python 3.10 or later:

```bash
python -m venv .venv
```

Activate the virtual environment (`.venv\Scripts\activate` on Windows or
`source .venv/bin/activate` on macOS/Linux), then install and start the app:

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive Swagger docs and
the generated OpenAPI schema are at `/docs` and `/openapi.json`.

## Schemas

`WeatherResponse` contains:

| Field | Type | Description |
| --- | --- | --- |
| `temperature` | number | Forecast temperature in the requested unit. |
| `humidity` | integer | Relative humidity percentage. |
| `condition` | string | Short weather condition. |
| `timestamp` | string (`date-time`) | UTC time associated with the sample forecast. |

`WeatherAlertRequest` contains two required string fields:

| Field | Type |
| --- | --- |
| `severity` | string |
| `message` | string |

## Routes

### `GET /weather/{city}`

Returns a `WeatherResponse` for `london`, `new york`, or `tokyo` (city
matching is case-insensitive). The optional `unit` query parameter accepts `C`
or `F` and defaults to `C`; an unsupported unit returns `422`. Unknown cities
return `404`.

Example happy path:

```bash
curl "http://127.0.0.1:8000/weather/London"
```

### `POST /weather/alerts`

Accepts a JSON `WeatherAlertRequest` and returns the validated request with
status `201 Created`. The request must include an `Authorization: Bearer
<token>` header. Any non-empty bearer token is accepted; this sample service
does not validate tokens against an identity provider. Missing or malformed
bearer authentication returns `401`; an invalid request body returns `422`.

Example sad path (missing token; expected `401 Unauthorized`):

```bash
curl -i -X POST "http://127.0.0.1:8000/weather/alerts" \
  -H "Content-Type: application/json" \
  -d '{"severity":"high","message":"Severe wind warning"}'
```
