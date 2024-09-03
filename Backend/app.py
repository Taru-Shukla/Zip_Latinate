from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import pandas as pd

app = Flask(__name__)

# Apply CORS to the entire app
cors = CORS(app, resources={r'/*': {
    'origins': 'https://zip-latinate-frontend.onrender.com',
    'methods': ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    'allow_headers': ["Content-Type", "Authorization", "X-Requested-With"],
    'supports_credentials': True
}})
app.config['CORS_HEADERS'] = 'Content-Type'

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
    
    result = df[df['zip'] == zip_code]
    if not result.empty:
        county = result.iloc[0]['county_name']
        latitude = result.iloc[0]['lat']
        longitude = result.iloc[0]['lng']
        population = result.iloc[0]['population']
        return {"county": county, "latitude": latitude, "longitude": longitude, "population": population}
    return None

@app.route('/api/convert_name', methods=['POST'])
@cross_origin()
def convert_name():
    try:
        data = request.get_json()  # Get JSON data
        if not data or 'name' not in data:
            return make_cors_response(jsonify({'error': 'Name not provided'}), 400)

        name = data.get('name', '')
        pig_latin_name = pig_latin(name)
        response = jsonify({'pig_latin_name': pig_latin_name})
        return make_cors_response(response, 200)
    except Exception as e:
        response = jsonify({'error': str(e)})
        return make_cors_response(response, 500)

@app.route('/api/zipcode_info', methods=['POST'])
@cross_origin()
def zipcode_info():
    try:
        data = request.get_json()  # Get JSON data
        if not data or 'zip_code' not in data:
            return make_cors_response(jsonify({'error': 'Zip code not provided'}), 400)

        zipcode = data.get('zip_code', '').zfill(5)  # Ensure zip code is 5 digits
        info = zip_code_pop(zipcode)
        if info:
            response = jsonify(info)
            return make_cors_response(response, 200)
        return make_cors_response(jsonify({"error": "Zip code not found"}), 404)
    except Exception as e:
        response = jsonify({'error': str(e)})
        return make_cors_response(response, 500)

def make_cors_response(response, status=200):
    # This function ensures that the correct CORS headers are added to each response
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
    return response, status

if __name__ == '__main__':
    app.run(debug=True)