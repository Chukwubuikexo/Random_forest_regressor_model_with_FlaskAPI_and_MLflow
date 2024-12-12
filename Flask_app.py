from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model and feature names
model = joblib.load("random_forest_model.pkl")
feature_names = model.feature_names_in_  # Get the features the model expects

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse the JSON input
        input_data = request.get_json()
        input_df = pd.DataFrame(input_data)
l
        # Ensure all expected features are present
        for feature in feature_names:
            if feature not in input_df.columns:
                input_df[feature] = 0  # Fill missing features with a default value (e.g., "0")
        
        # Ensure column order matches the training data
        input_df = input_df[feature_names]

        # Make predictions
        predictions = model.predict(input_df)
        return jsonify({'predictions': predictions.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
