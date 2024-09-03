from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)

# CORS Configuration
# This will allow CORS for all routes with specific settings
CORS(app, resources={r"/*": {
    "origins": ["https://zip-latinate-frontend.onrender.com"],  # Restricting to your frontend's origin
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allowed methods
    "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],  # Allowed headers
    "supports_credentials": True  # If you need to allow credentials (cookies, authorization headers)
}})

def pig_latin(name):
    vowels = "aeiou"
    name = name.lower()
    words = name.split()
    pig_latin_words = []

    for word in words:
        if any(char.isdigit() for char in word):
            pig_latin_words.append(word)
        elif word[0] in vowels:
            pig_latin_words.append(word + "yay")
        else:
            pig_latin_words.append(word[1:] + word[0] + "ay")
    return " ".join(pig_latin_words)

def zip_code_pop(zip_code):
    df = pd.read_csv('uszips.csv')
    df['zip'] = df['zip'].astype(str).str.strip().str.zfill(5)  # Ensure zip codes are strings with leading zeros
    
    print(f"Searching for Zipcode: {zip_code}")
    print(df['zip'].head(10))  # Print the first 10 zip codes to verify formatting
    print(df[df['zip'] == zip_code])  # Debugging print

    result = df[df['zip'] == zip_code]
    if not result.empty:
        county = result.iloc[0]['county_name']
        latitude = result.iloc[0]['lat']
        longitude = result.iloc[0]['lng']
        population = result.iloc[0]['population']
        return {"county": county, "latitude": latitude, "longitude": longitude, "population": population}
    return None

@app.route('/api/convert_name', methods=['POST'])
def convert_name():
    data = request.json
    name = data.get('name', '')
    pig_latin_name = pig_latin(name)  # Implement this function based on your logic
    return jsonify({'pig_latin_name': pig_latin_name})

@app.route('/api/zipcode_info', methods=['POST'])
def zipcode_info():
    data = request.json
    zip_code = data.get('zip_code', '')
    # Implement your logic to fetch county and coordinates based on the zip code
    response_data = {
        'latitude': 40.7128,  # Example latitude
        'longitude': -74.0060,  # Example longitude
        'county': 'New York'  # Example county
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)