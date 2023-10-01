# Points Tracker API

The Points Tracker API is a simple Flask application that allows you to manage and track point transactions. Built using Python and SQLite, it offers a lightweight solution for adding, spending, and checking balance of points for different payers.

## Prerequisites

- Python (3.6 or higher is recommended)
- Flask
- SQLite

## Getting Started

1. **Setting Up the Environment**:
    - Clone the repository to your local machine.
    - Navigate to the directory where the application files are located.
    - It's recommended to use a virtual environment. Set it up using:
      ```
      python -m venv venv
      ```
    - or 
        ```
        python3 -m venv venv
        ```
    - Activate the virtual environment:
      - On Windows: `venv\Scripts\activate` 
      - or `. .\venv\Scripts\Activate` in powershell
      - On macOS and Linux: `source venv/bin/activate`

2. **Install Dependencies**:
    After activating the virtual environment, install the required packages:
    ```
    pip install flask
    ```

3. **Setting Up the Database**:
    Before running the application for the first time, ensure the SQLite database `pointsTracker.sqlite` is set up and the `transactions` table is created. Do so with:
    ```
    python db.py
    ```

4. **Running the Application**:
    With everything set up, run the application using:
    ```
    python app.py
    ```
    This will start the Flask server, and the API will be accessible at `http://127.0.0.1:8000/`.

## Endpoints

All endpoints accept parameters in the form of `form-data`.

1. **Add Points**:
    - **URL**: `/add`
    - **Method**: `POST`
    - **Data Params**: 
      - `payer`: Name of the payer
      - `points`: Points to be added (can be negative)
      - `timestamp`: Timestamp of the transaction in the format `%Y-%m-%dT%H:%M:%SZ`
    
2. **Spend Points**:
    - **URL**: `/spend`
    - **Method**: `POST`
    - **Data Params**: 
      - `points`: Points to be spent

3. **Get Balance**:
    - **URL**: `/balance`
    - **Method**: `GET`