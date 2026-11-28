# Weather API Reference

**Base URL:** `http://127.0.0.1:8000`

The API provides deterministic sample forecasts for London, New York, and
Tokyo, and accepts weather alerts. Interactive documentation and the generated
OpenAPI schema are available at `/docs` and `/openapi.json` while the service
is running.

## `GET /cities`

Returns the list of supported cities.

### Response

`200 OK` — A JSON array of supported city names.

```json
["london", "new york", "tokyo"]
```

### Example

```bash
curl "http://127.0.0.1:8000/cities"
```

## `GET /weather/{city}`

Returns the forecast for a supported city. City matching is case-insensitive
and ignores surrounding whitespace.

### Parameters

| Name   | In    | Required | Values                             | Default | Description                 |
| ------ | ----- | -------- | ---------------------------------- | ------- | --------------------------- |
| `city` | path  | Yes      | `london`, `new york`, `tokyo`      | —       | City to retrieve.           |
| `unit` | query | No       | `C`, `F`                           | `C`     | Celsius or Fahrenheit.      |

Any `unit` value other than `C` or `F` returns `422 Unprocessable Entity`.

### Responses

#### `200 OK`

Returns a `WeatherResponse` object.

| Field         | Type             | Required | Description                                   |
| ------------- | ---------------- | -------- | --------------------------------------------- |
| `temperature` | number           | Yes      | Sample temperature in the requested unit.     |
| `humidity`    | integer          | Yes      | Relative humidity percentage.                 |
| `condition`   | string           | Yes      | Short weather condition.                      |
| `timestamp`   | string (date-time)| Yes      | UTC timestamp associated with the forecast.   |
| `wind_speed_kmh` | number        | Yes      | Wind speed in kilometers per hour.            |

```json
{
  "temperature": 54.5,
  "humidity": 78,
  "condition": "Cloudy",
  "timestamp": "2026-11-25T00:00:00Z",
  "wind_speed_kmh": 15.0
}
```

#### `404 Not Found`

Returned when no forecast is available for the requested city.

```json
{
  "detail": "No forecast available for city 'Paris'."
}
```

#### `422 Unprocessable Entity`

Returned when a query parameter fails validation. The response includes a
`detail` array containing validation errors.

### Example

```bash
curl "http://127.0.0.1:8000/weather/London?unit=F"
```

## `POST /weather/alerts`

Submits a weather alert. The API returns the validated request body; it does
not persist or dispatch alerts.

### Authentication

Send a non-empty bearer token in the `Authorization` header:

```http
Authorization: Bearer <token>
```

This sample API only checks that the bearer token is present and non-empty. It
does not validate the token with an identity provider.

### Request body

**Content type:** `application/json`

A `WeatherAlertRequest` requires both fields:

| Field      | Type   | Required | Description      |
| ---------- | ------ | -------- | ---------------- |
| `severity` | string | Yes      | Alert severity.  |
| `message`  | string | Yes      | Alert message.   |

**Example:**

```json
{
  "severity": "high",
  "message": "Severe wind warning"
}
```

### Responses

#### `201 Created`

Returns the submitted `WeatherAlertRequest` as JSON.

```json
{
  "severity": "high",
  "message": "Severe wind warning"
}
```

#### `401 Unauthorized`

Returned when the bearer token is missing, malformed, or empty. The response
includes the `WWW-Authenticate: Bearer` header.

```json
{
  "detail": "A bearer token is required."
}
```

#### `422 Unprocessable Entity`

Returned when the request body is missing or fails schema validation, such as
when a required field is omitted. The response includes a `detail` array
containing validation errors.

### Example

```bash
curl -X POST "http://127.0.0.1:8000/weather/alerts" \
  -H "Authorization: Bearer example-token" \
  -H "Content-Type: application/json" \
  -d '{"severity":"high","message":"Severe wind warning"}'
```
