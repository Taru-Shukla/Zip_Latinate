from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://zip-latinate-frontend.onrender.com"}})

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

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@app.route('/convert_name', methods=['POST'])
def convert_name():
    try:
        name = request.json['name']
        return jsonify({"pig_latin_name": pig_latin(name)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/zipcode_info', methods=['POST'])
def zipcode_info():
    try:
        zipcode = request.json.get('zip_code', '').zfill(5)  # Ensure zip code is 5 digits
        info = zip_code_pop(zipcode)
        if info:
            return jsonify(info)
        return jsonify({"error": "Zip code not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
# @app.route('/convert_name', methods=['POST'])
# def convert_name():
#     name = request.json['name']
#     return jsonify({"pig_latin_name": pig_latin(name)})

# @app.route('/zipcode_info', methods=['POST'])
# def zipcode_info():
#     zipcode = request.json.get('zip_code', '').zfill(5)  # Ensure zip code is 5 digits
#     print(f"Received Zipcode: {zipcode}")  # Debugging print

#     info = zip_code_pop(zipcode)
#     if info:
#         return jsonify(info)
#     return jsonify({"error": "Zip code not found"}), 404

# if __name__ == '__main__':
#     app.run(debug=True)
