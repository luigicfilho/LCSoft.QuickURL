# LCSoft URL Shortener

A professional URL shortening service built with **FastAPI**, focused on security, performance, and maintainability. This project demonstrates best practices for modern Python web APIs including async ORM integration, JWT authentication, rate limiting, and automated testing.

> [!NOTE]
> This project was created in a weekend, so with a time limit constraint, so there is somethings missing and not complete, take this as a test of skills.

---

## Features

- Shorten URLs with customizable expiration
- Redirect short URLs to target URLs with click tracking
- Admin API to list, delete URLs and view statistics
- JWT-secured admin endpoints with strict token validation
- Rate limiting to prevent abuse (global and route-specific)
- CORS configured for trusted domains only
- Centralized async ORM lifecycle management with Tortoise-ORM
- Pydantic validation for request data and business rules
- Comprehensive logging with trace/correlation IDs
- Automated tests with pytest, HTTPX, and in-memory SQLite
- Coverage reporting and code quality enforcement with linters and type checks

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/)
- [Pydantic](https://pydantic.dev/)
- [Pytest](https://pytest.org/)
- [HTTPX](https://www.python-httpx.org/)
- [SlowAPI](https://slowapi.readthedocs.io/en/latest/)
- [JWT (PyJWT)](https://pyjwt.readthedocs.io/en/stable/)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/luigicfilho/LCSoft.QuickURL.git
cd LCSoft.QuickURL
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create .env file with your settings (example):

```ini
DATABASE_URL=sqlite://db.sqlite3
JWT_SECRET=supersecretadmin
CORS_ALLOWED_ORIGINS=["http://localhost:8000", "https://yourdomain.com"]
```

## Running the Application
```bash
uvicorn app.main:app --reload
```

The API docs will be available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Generating Auth Token
To test the Admin endpoints, generate the JWT token with the command:

```bash
python -m app.utils.generate_token
```

## Usage

Public Endpoints
- POST /api/v1/urls/shorten: Create a new short URL
- GET /api/v1/urls/{code}: Redirect to the target URL

Admin Endpoints (Require JWT Bearer Token)
- GET /api/v1/admin/urls: List all URLs
- DELETE /api/v1/admin/urls/{code}: Delete a URL by code
- GET /api/v1/admin/stats/{code}: Get statistics for a URL

## Testing
Run all tests with coverage:

```bash
pytest
```

Generate coverage report:

```bash
pytest --cov=app --cov-report=term --cov-report=html
```

## Code Quality
The project uses:
- ruff for linting
- black for formatting
- mypy for static type checking

Run linters and formatters via:

```bash
ruff check .
black .
mypy .
```

## Architecture Highlights
- Modular design: separate layers for models, schemas, services, routers, and extensions
- Async lifecycle management for DB connections using FastAPI lifespan context
- Dependency injection with FastAPI’s Depends()
- Custom middleware for rate limiting and trace ID injection
- Pydantic validators enforce business rules (e.g., max URL expiration)
- Centralized logging with configurable formats and correlation IDs

## Future Improvements
- JWT token revocation with blacklist support (via JTI)
- Enhanced security headers middleware (like Helmet.js for FastAPI)
- Monitoring integration with Prometheus and Grafana
- Admin UI with Blazor or FastAPI UI
- Scaling database backend for clustering and high availability

## License
This project is licensed under the CC BY-NC-ND 4.0.

## Contact
For support or inquiries, please contact:
LCSoft API Support
