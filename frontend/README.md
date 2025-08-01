
# Frontend

This is the frontend of the project, built with React. It provides the user interface for interacting with the automated research paper generation system.

## Workflow

The frontend is a single-page application (SPA) that communicates with the backend to fetch data and trigger actions. Here's a breakdown of the key files and their roles:

-   **`main.jsx`**: The entry point of the application. It renders the `App` component into the DOM.
-   **`App.jsx`**: The root component that sets up the application's routing. It uses `react-router-dom` to define routes for different pages.
-   **`apiService.js`**: A dedicated module for making API calls to the backend. All communication with the server is centralized here.
-   **`pages/`**: This directory contains the main pages of the application:
    -   **`HomePage.jsx`**: The landing page of the application.
    -   **`DashboardPage.jsx`**: The main dashboard where users can generate research papers, view history, and manage their work.
    -   **`SettingsPage.jsx`**: A page for user settings and application configuration.
-   **`components/`**: This directory contains reusable UI components:
    -   **`Layout.jsx`**: A component that defines the overall layout of the application, including the navigation bar and footer.
    -   **`ShowcaseGraphic.jsx`**: A component used on the `HomePage` to display a graphic or animation.

## Setup

To run the frontend locally, follow these steps:

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```

This will start the development server, and you can view the application in your browser at `http://localhost:5173`.
