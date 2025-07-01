from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS to allow requests from the frontend HTML file
CORS(app)

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


@app.route('/forecast', methods=['POST'])
def get_forecast():
    """
    API endpoint to receive data and return a forecast.
    """
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
