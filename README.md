# Airport API — Functional Overview and Access Instructions

## Functional Capabilities

### User Authentication & Authorization

* JWT-based authentication with access and refresh tokens
* Endpoints for user registration, login, logout, and token refresh
* Role-based access control for staff vs regular users

### Airport Management

* CRUD operations for countries, cities, airports, airplanes, and airplane types
* Restriction: creation and modification of airport-related data limited to admin/staff users

### Flight and Crew Management

* CRUD for routes, flights, crews — accessible only to authorized personnel
* Validation rules (e.g., no flights scheduled in the past)

### Ticketing and Orders

* Users can create, update, and delete their own tickets
* Orders created automatically based on tickets purchased

### API Security and Stability

* Proper error handling with standardized HTTP status codes (401 for unauthorized, 403 for forbidden, etc.)
* CORS configured to allow frontend integrations
* Rate limiting to prevent abuse (if implemented)

---

## Setup and Access Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd airport-api
    ```

2.  **Set up environment variables:**
    Copy `.env.example` to `.env` and fill in required values (database credentials, secret keys, etc.)

3.  **Start services with Docker Compose:**
    ```bash
    docker-compose up -d
    ```

4.  **Apply migrations:**
    ```bash
    docker-compose exec app python manage.py migrate
    ```

5.  **Create a superuser for admin access (optional):**
    ```bash
    docker-compose exec app python manage.py createsuperuser
    ```

6.  **Access the API:**
    * The API server runs at `http://localhost:8000/`
    * Admin panel available at `http://localhost:8000/admin/`
    * Use the documented endpoints to register, authenticate, and interact with airport and flight data

7.  **Testing authentication:**
    * Obtain JWT token by POSTing credentials to `/api/auth/login/`
    * Use the access token in the `Authorization: Bearer <token>` header for protected endpoints
