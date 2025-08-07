from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_cors import CORS
import os

app = Flask(__name__)
# Enable CORS to allow requests from the frontend HTML file
CORS(app)

# A secret key is required for session management.
# In a production app, you should set this from an environment variable.
app.secret_key = os.urandom(24)

# Simple in-memory user store for demonstration purposes.
USERS = {
    "admin": "password"
}

def simple_moving_average(data, window):
    """
    Calculates the next 4 quarters using Simple Moving Average.
    """
    if not data or window <= 0 or window > len(data):
        return []
    
    forecasts = []
    # Use the last 'window' data points to start forecasting
    current_data = list(data)

    for _ in range(4): # Forecast for the next 4 quarters
        # Calculate the average of the last 'window' periods
        forecast_value = sum(current_data[-window:]) / window
        forecasts.append(forecast_value)
        # Add the new forecast to the data series to be used for the next forecast
        current_data.append(forecast_value)
        
    return forecasts

def exponential_smoothing(data, alpha):
    """
    Calculates the next 4 quarters using Single Exponential Smoothing.
    """
    if not data or not (0 <= alpha <= 1):
        return []

    # Start with the first data point as the initial forecast
    forecasts = [data[0]] 
    for i in range(1, len(data)):
        # The standard ES formula
        last_forecast = forecasts[-1]
        new_forecast = alpha * data[i-1] + (1 - alpha) * last_forecast
        forecasts.append(new_forecast)
    
    # Now, forecast for the next 4 quarters
    future_forecasts = []
    last_known_forecast = forecasts[-1]
    
    for i in range(len(data), len(data) + 4):
        # For future periods, the forecast is the last calculated forecast value
        # updated with the most recent actual data point.
        future_forecast = alpha * data[-1] + (1 - alpha) * last_known_forecast
        future_forecasts.append(future_forecast)
        # For single ES, the future forecasts will all be the same value
        # as we don't have new "actuals" to update the forecast.
        # So we update the last_known_forecast to be this new value for consistency,
        # though it won't change the result for single ES.
        last_known_forecast = future_forecast

    return future_forecasts

@app.route('/')
def index():
    """
    Serves the main forecasting page, but only if the user is logged in.
    Otherwise, it redirects to the login page.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login. Shows the login form on GET and processes credentials on POST.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if user exists and password is correct
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Logs the user out by clearing the session.
    """
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/forecast', methods=['POST'])
def get_forecast():
    """
    API endpoint to receive data and return a forecast.
    """
    # Protect this endpoint to ensure only logged-in users can get a forecast.
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        payload = request.get_json()
        data = payload.get('data')
        method = payload.get('method')
        params = payload.get('params')

        if not data or not method or not params:
            return jsonify({"error": "Missing data, method, or parameters"}), 400

        if method == 'sma':
            window = params.get('window')
            if window is None:
                return jsonify({"error": "Missing 'window' parameter for SMA"}), 400
            result = simple_moving_average(data, int(window))
        elif method == 'es':
            alpha = params.get('alpha')
            if alpha is None:
                return jsonify({"error": "Missing 'alpha' parameter for ES"}), 400
            result = exponential_smoothing(data, float(alpha))
        else:
            return jsonify({"error": f"Unknown method: {method}"}), 400

        return jsonify({"forecast": result})

    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


if __name__ == '__main__':
    # Runs the Flask app on localhost, port 5000
    app.run(debug=True)
