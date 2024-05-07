# Radio Tracking System

Radio Tracking System is a web-based application built with Flask for tracking radios at the harbor.

## Features

- **Login**: Users can log in to access the system.
- **Dashboard**: Displays a list of radios with their details such as ID, model, status, current user, and action buttons for checking in/out radios.
- **Radio Tracking**: Allows users to check in/out radios.

## Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.x
- Flask
- SQLite

## Getting Started

1. Clone this repository to your local machine:

    ```
    git clone https://github.com/Tsikoviski/R_track_2
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Set up the database:

    ```
    python create_database.py
    ```

4. Run the application:

    ```
    python app.py
    ```

5. Open your web browser and go to `http://localhost:5000` to access the application.

## Usage

- Log in using your username and password.
- View the dashboard to see a list of radios.
- Check in/out radios by clicking the respective buttons in the dashboard.

## Acknowledgements

- Flask
- SQLite

---
