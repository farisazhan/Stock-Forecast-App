# Warehouse Stock Forecasting

A simple web application to forecast future warehouse stock levels based on historical data. This tool implements two common forecasting methods: Simple Moving Average (SMA) and Exponential Smoothing (ES).

The frontend is a single HTML file using Tailwind CSS and vanilla JavaScript, and the backend is a lightweight Flask server.

## Features

- **Dynamic Data Entry**: Input historical quarterly stock data for one or more years.
- **Forecasting Methods**: Choose between Simple Moving Average (SMA) and Exponential Smoothing (ES).
- **Customizable Parameters**: Adjust the moving average window for SMA or the alpha smoothing factor for ES.
- **Instant Forecasts**: Generate and view the stock forecast for the next four quarters.
- **Clean UI**: The user interface is built with Tailwind CSS for a modern and responsive experience.
- **Clear Error Handling**: Provides user-friendly messages for invalid inputs.

## Tech Stack

- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Backend**: Python, Flask

## Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

- Python 3.x
- `pip` (Python package installer)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Set up a Python virtual environment (recommended):**

    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate it
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install the backend dependencies:**

    Create a file named `requirements.txt` with the following content:
    ```
    Flask
    Flask-Cors
    ```

    Then, install the packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the backend server:**

    Execute the `app.py` file:
    ```bash
    python app.py
    ```
    The server will start on `http://127.0.0.1:5000`.

5.  **Launch the frontend:**
    
    Open the `index.html` file in your web browser.

## How to Use

1.  Open `index.html` in your browser.
2.  Enter the historical quarterly stock data. Use the "Add Another Year" button if you need more input fields.
3.  Select a forecasting method (Simple Moving Average or Exponential Smoothing).
4.  Adjust the parameters for the selected method (e.g., the "Window" for SMA).
5.  Click the "Generate Forecast" button.
6.  The forecasted stock levels for the next four quarters will appear at the bottom of the page.

## API Endpoint

The application uses a single API endpoint to perform the calculations.

### `POST /forecast`

Accepts historical data and forecasting parameters and returns a 4-quarter forecast.

**Request Body Example:**
```json
{
  "data": [100, 110, 105, 120],
  "method": "sma",
  "params": { "window": 3 }
}
```

**Success Response Example:**
```json
{
  "forecast": [111.67, 115.56, 115.74, 114.32]
}
```