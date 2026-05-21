Task Management FastAPI (demo)
---
---
Quick demo project showing a minimal FastAPI structure with SQLAlchemy.


### Create a virtual environment with all necessary dependencies

From the root of the project execute:

```bash
uv sync
```

## Run application

### Development mode

```bash
uv run fastapi dev
# then open http://127.0.0.1:8000/scalar for the offline Scalar API explorer
```

### Production mode

```bash
uv run fastapi run
```


SMS.ir configuration

Set this environment variable to enable real SMS delivery:

```bash
export SMSIR_API_KEY="your-smsir-api-key"
export SMSIR_LINE_NUMBER="your-line-number"  # optional
```

The app will authenticate outgoing SMS requests using the `X-API-KEY` header.

User OTP Sign-in

- POST `/users/otp/send` with JSON `{ "phone_number": "+15551234567" }`
- POST `/users/otp/verify` with JSON `{ "phone_number": "+15551234567", "code": "123456" }`

Tests

```bash
uv run pytest -q
```
