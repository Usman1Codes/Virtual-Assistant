
# Backend

This is the backend of the project, built with FastAPI. It serves as the API for the frontend and handles the core logic of the automated research paper generation system.

## Workflow

The backend is a Python-based API server that exposes several endpoints for the frontend to consume. Here's a breakdown of the key files and their roles:

-   **`main.py`**: The entry point of the application. It initializes the FastAPI app and includes the API routers.
-   **`requirements.txt`**: This file lists all the Python dependencies required to run the backend.
-   **`auth_helper.py`**: Contains helper functions for authentication and authorization.
-   **`api/`**: This directory contains the API endpoints:
    -   **`auth.py`**: Handles user authentication, registration, and token management.
    -   **`assistant.py`**: Provides endpoints for interacting with the AI assistant.
    -   **`conversations.py`**: Manages conversation history with the assistant.
    -   **`config.py`**: Contains configuration for the API.
    -   **`email.py`**: Exposes endpoints for sending emails.
-   **`core/`**: This directory contains the core logic and database models:
    -   **`database.py`**: Sets up the database connection.
    -   **`models.py`**: Defines the SQLAlchemy database models.
    -   **`schemas.py`**: Contains Pydantic schemas for data validation and serialization.
    -   **`engine.py`**: The core logic of the research paper generation process.
    -   **`config.py`**: Core application configuration.
-   **`services/`**: This directory contains services for interacting with external systems:
    -   **`ai_service.py`**: A service for communicating with the AI model (e.g., OpenAI).
    -   **`email_service.py`**: A service for sending emails.
    -   **`sheets_service.py`**: A service for interacting with Google Sheets.

## Prerequisites

Before running the backend, you need to configure your Google Cloud Platform project and enable the necessary APIs. This is required for sending and receiving emails (Gmail API) and for writing data to Google Sheets (Google Sheets API).

### Google Cloud Platform Setup

1.  **Create a Google Cloud Project:** If you don't have one already, create a new project in the [Google Cloud Console](https://console.cloud.google.com/).

2.  **Enable APIs:** For your project, enable the following APIs:
    *   **Gmail API:** Allows the application to read and send emails.
    *   **Google Sheets API:** Allows the application to read and write data to Google Sheets.
    You can enable them by searching for them in the "APIs & Services" > "Library" section of the console.

3.  **Create Credentials:**
    *   Go to "APIs & Services" > "Credentials".
    *   Click "Create Credentials" and choose "OAuth client ID".
    *   Select "Desktop application" as the application type.
    *   Once created, download the JSON file. It is often named `credentials.json`.
    *   **Important:** You will need to place this file in the `backend` directory. The application is configured to look for it to authenticate with Google's services.

4.  **OAuth Consent Screen:** You will also need to configure the OAuth consent screen. For testing, you can add your own Google account as a test user.

## Setup

To run the backend locally, follow these steps:

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the development server:**
    ```bash
    uvicorn main:app --reload
    ```

This will start the development server, and you can access the API documentation at `http://localhost:8000/docs`. 