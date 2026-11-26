# Weather API reference

Base URL: `http://127.0.0.1:8000`

The API provides deterministic sample forecasts for London, New York, and
Tokyo, and accepts weather alerts. Interactive documentation and the generated
OpenAPI schema are available at `/docs` and `/openapi.json` when the service is
running.

## `GET /weather/{city}`

Returns the forecast for a supported city. City matching is case-insensitive
and ignores surrounding whitespace.

### Parameters

| Name | In | Required | Values | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `city` | path | Yes | `london`, `new york`, `tokyo` | — | City to retrieve. |
| `unit` | query | No | `C`, `F` | `C` | Temperature unit: Celsius or Fahrenheit. |

Any other `unit` value returns `422 Unprocessable Entity`.

### Responses

**`200 OK`** — A `WeatherResponse` object:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `temperature` | number | Yes | Sample forecast temperature, in the requested unit. |
| `humidity` | integer | Yes | Relative humidity percentage. |
| `condition` | string | Yes | Short weather condition. |
| `timestamp` | string (`date-time`) | Yes | UTC timestamp associated with the sample forecast. |

**`404 Not Found`** — No forecast is available for the requested city.

**`422 Unprocessable Entity`** — A query parameter failed validation, such as
an unsupported `unit` value. The response has a `detail` array with validation
errors.

### Example

```bash
curl "http://127.0.0.1:8000/weather/London?unit=F"
```

## `POST /weather/alerts`

Submits a weather alert. The API returns the validated request body; it does
not persist or dispatch alerts.

### Authentication

Send a non-empty bearer token in the `Authorization` header:

```text
Authorization: Bearer <token>
```

This sample API only checks that the bearer token is present and non-empty. It
does not validate the token with an identity provider.

### Request body

Content type: `application/json`

`WeatherAlertRequest` requires both fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `severity` | string | Yes | Alert severity. |
| `message` | string | Yes | Alert message. |

Example:

```json
{
  "severity": "high",
  "message": "Severe wind warning"
}
```

### Responses

**`201 Created`** — Returns the submitted `WeatherAlertRequest` as JSON.

**`401 Unauthorized`** — The bearer token is missing, malformed, or empty. The
response includes `WWW-Authenticate: Bearer`.

**`422 Unprocessable Entity`** — The request body is missing or fails schema
validation, such as when a required field is omitted. The response has a
`detail` array with validation errors.

### Example

```bash
curl -X POST "http://127.0.0.1:8000/weather/alerts" \
  -H "Authorization: Bearer example-token" \
  -H "Content-Type: application/json" \
  -d '{"severity":"high","message":"Severe wind warning"}'
```
