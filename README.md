# Airport API

This API provides access to airport-related data, allowing users to retrieve and manage information about airports, flights, and potentially other related entities.

## Key Features (Based on PR #1)

* **[List Feature 1 from PR]:** Briefly describe the first main functionality introduced or modified in this PR. *For example: Retrieve a list of all airports.*
* **[List Feature 2 from PR]:** Briefly describe the second main functionality. *For example: Get detailed information for a specific airport by its ID.*
* **[List Feature 3 from PR]:** Briefly describe the third main functionality. *For example: Add new airport data.*
* **(Add more features as implemented in the PR)**

---

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* [Python](https://www.python.org/downloads/) (specify version, e.g., 3.9+)
* [Pip](https://pip.pypa.io/en/stable/installation/)
* [Git](https://git-scm.com/downloads)
* [Docker](https://www.docker.com/get-started) (for Docker-based setup)

---

### Installation via GitHub

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Danylo-D87/airport-api.git](https://github.com/Danylo-D87/airport-api.git)
    cd airport-api
    ```

2.  **Switch to the relevant branch (if the PR is not merged to main yet):**
    ```bash
    git fetch origin pull/1/head:pr1
    git checkout pr1
    ```
    *(Alternatively, if you know the branch name for PR #1, checkout that branch directly after cloning)*

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
    * On Windows:
        ```bash
        venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure you have a `requirements.txt` file in your project root. If not, list the main dependencies here or instruct how to install them, e.g., `pip install flask flask-sqlalchemy ...`)*

5.  **Set up environment variables (if any):**
    Create a `.env` file in the project root and add any necessary environment variables. For example:
    ```env
    DATABASE_URL=your_database_connection_string
    SECRET_KEY=your_secret_key
    # Add other variables as needed
    ```
    *(Mention if there's an example environment file, e.g., `.env.example`)*

6.  **Run database migrations (if applicable):**
    *(If using a database like PostgreSQL with an ORM like SQLAlchemy and Alembic)*
    ```bash
    # Example commands, adjust to your project's tools (e.g., Flask-Migrate, Alembic)
    # flask db init  (if first time)
    # flask db migrate -m "Initial migration"
    # flask db upgrade
    ```

7.  **Run the application:**
    ```bash
    # Example for Flask, adjust if using Django, FastAPI, etc.
    python app.py
    # or
    # flask run
    ```
    The API should now be running on `http://127.0.0.1:5000` (or your configured host and port).

---

### Running via Docker

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone [https://github.com/Danylo-D87/airport-api.git](https://github.com/Danylo-D87/airport-api.git)
    cd airport-api
    ```

2.  **Switch to the relevant branch (if the PR is not merged to main yet):**
    ```bash
    git fetch origin pull/1/head:pr1
    git checkout pr1
    ```

3.  **Ensure you have a `Dockerfile` and `docker-compose.yml` (if using Compose) in your project root.**

    * **Example `Dockerfile` (simple Flask app):**
        ```dockerfile
        # Use an official Python runtime as a parent image
        FROM python:3.9-slim

        # Set the working directory in the container
        WORKDIR /app

        # Copy the current directory contents into the container at /app
        COPY . /app

        # Install any needed packages specified in requirements.txt
        RUN pip install --no-cache-dir -r requirements.txt

        # Make port 5000 available to the world outside this container
        EXPOSE 5000

        # Define environment variable
        ENV NAME World

        # Run app.py when the container launches
        CMD ["python", "app.py"]
        ```
        *(Adjust this Dockerfile to your project's specific needs, including environment variables, entrypoint scripts, etc.)*

    * **Example `docker-compose.yml` (if you have multiple services like a DB):**
        ```yaml
        version: '3.8'
        services:
          web:
            build: .
            ports:
              - "5000:5000" # Host:Container
            volumes:
              - .:/app
            # environment: # You can also pass environment variables here or through an .env file
            #   - FLASK_ENV=development
            #   - DATABASE_URL=your_db_url_for_docker_container
            # depends_on:
            #   - db # if you have a database service
          # db:
          #   image: postgres:13
          #   volumes:
          #     - postgres_data:/var/lib/postgresql/data/
          #   environment:
          #     - POSTGRES_USER=user
          #     - POSTGRES_PASSWORD=password
          #     - POSTGRES_DB=mydb
        # volumes:
        #   postgres_data:
        ```
        *(This is a basic example. You'll need to configure it for your database, environment variables, and other services.)*

4.  **Build and run the Docker container(s):**

    * **Using Dockerfile directly:**
        ```bash
        docker build -t airport-api .
        docker run -p 5000:5000 airport-api
        ```
        *(If you need to pass environment variables, use the `-e` flag or an `--env-file`)*
        ```bash
        # Example with an .env file
        # docker run --env-file ./.env -p 5000:5000 airport-api
        ```

    * **Using Docker Compose:**
        ```bash
        docker-compose up --build
        ```
        *(Docker Compose will automatically look for `.env` file in the project root to load environment variables for the services defined in `docker-compose.yml`)*

5.  The API should now be running and accessible, typically on `http://localhost:5000`.

---

## API Endpoints

*(It's good practice to list your main API endpoints here once they are stable. Refer to your API documentation (e.g., Swagger/OpenAPI spec) for a full list.)*

**Example:**

* `GET /airports` - Retrieves a list of all airports.
* `GET /airports/{airport_id}` - Retrieves details for a specific airport.
* `POST /airports` - Adds a new airport.
    * **Body:** (application/json)
        ```json
        {
          "name": "New Century AirCenter",
          "iata_code": "JCI",
          "city": "Olathe",
          "country": "USA"
        }
        ```

---
---
