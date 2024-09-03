from flask import Flask, request, jsonify, make_response
import pandas as pd

app = Flask(__name__)

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

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response('', 204)
        response.headers['Access-Control-Allow-Origin'] = 'https://zip-latinate-frontend.onrender.com'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://zip-latinate-frontend.onrender.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/api/convert_name', methods=['POST'])
def convert_name():
    try:
        data = request.json
        name = data.get('name', '')
        pig_latin_name = pig_latin(name)
        response = jsonify({'pig_latin_name': pig_latin_name})
        return add_cors_headers(response)
    except Exception as e:
        response = jsonify({'error': str(e)})
        return add_cors_headers(response), 500

@app.route('/api/zipcode_info', methods=['POST'])
def zipcode_info():
    zipcode = request.json.get('zip_code', '').zfill(5)  # Ensure zip code is 5 digits
    info = zip_code_pop(zipcode)
    if info:
        response = jsonify(info)
        return add_cors_headers(response)
    return add_cors_headers(jsonify({"error": "Zip code not found"})), 404

if __name__ == '__main__':
    app.run(debug=True)