# from flask import Flask, request, jsonify, make_response
# from flask_cors import CORS, cross_origin
# import pandas as pd

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins" : "https://zip-latinate-frontend.onrender.com" }})

# @app.route("/api/", methods=['GET'])
# def home():
#     return "<h1> Zip Latinate </h1>"

# # Apply CORS to the entire app
# # cors = CORS(app, resources={r'/*': {
# #     'origins': 'https://zip-latinate-frontend.onrender.com',
# #     'methods': ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
# #     'allow_headers': ["Content-Type", "Authorization", "X-Requested-With"],
# #     'supports_credentials': True
# # }})
# # app.config['CORS_HEADERS'] = 'Content-Type'

# def pig_latin(name):
#     vowels = "aeiou"
#     name = name.lower()
#     words = name.split()
#     pig_latin_words = []

#     for word in words:
#         if any(char.isdigit() for char in word):
#             pig_latin_words.append(word)
#         elif word[0] in vowels:
#             pig_latin_words.append(word + "yay")
#         else:
#             pig_latin_words.append(word[1:] + word[0] + "ay")
#     return " ".join(pig_latin_words)

# # def zip_code_pop(zip_code):
# #     df = pd.read_csv('uszips.csv')
# #     df['zip'] = df['zip'].astype(str).str.strip().str.zfill(5)  # Ensure zip codes are strings with leading zeros
    
# #     result = df[df['zip'] == zip_code]
# #     if not result.empty:
# #         county = result.iloc[0]['county_name']
# #         latitude = result.iloc[0]['lat']
# #         longitude = result.iloc[0]['lng']
# #         population = result.iloc[0]['population']
# #         return {"county": county, "latitude": latitude, "longitude": longitude, "population": population}
# #     return None

# @app.route('/api/convert_name', methods=['POST'])
# # @cross_origin()
# def convert_name():
#     try:
#         data = request.get_json()  # Get JSON data
#         if not data or 'name' not in data:
#             return make_cors_response(jsonify({'error': 'Name not provided'}), 400)

#         name = data.get('name', '')
#         pig_latin_name = pig_latin(name)
#         #response = jsonify({'pig_latin_name': pig_latin_name})
#         response = "taruuuuu"
#         return make_cors_response(response, 200)
#     except Exception as e:
#         response = jsonify({'error': str(e)})
#         return make_cors_response(response, 500)

# # @app.route('/api/zipcode_info', methods=['POST'])
# # @cross_origin()
# # def zipcode_info():
# #     try:
# #         data = request.get_json()  # Get JSON data
# #         if not data or 'zip_code' not in data:
# #             return make_cors_response(jsonify({'error': 'Zip code not provided'}), 400)

# #         zipcode = data.get('zip_code', '').zfill(5)  # Ensure zip code is 5 digits
# #         info = zip_code_pop(zipcode)
# #         if info:
# #             response = jsonify(info)
# #             return make_cors_response(response, 200)
# #         return make_cors_response(jsonify({"error": "Zip code not found"}), 404)
# #     except Exception as e:
# #         response = jsonify({'error': str(e)})
# #         return make_cors_response(response, 500)

# def make_cors_response(response, status=200):
#     # This function ensures that the correct CORS headers are added to each response
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Credentials', 'true')
#     response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
#     return response, status

# if __name__ == '__main__':
#     app.run()

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://zip-latinate-frontend.onrender.com"])

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

# Standardized Response Format
def build_response(status, message, data=None):
    response_content = {
        'status': status,
        'message': message,
        'data': data
    }
    return jsonify(response_content)

@app.route('/api/convert_name', methods=['POST', 'OPTIONS'])
def convert_name():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    try:
        data = request.json  # Get JSON data
        if not data or 'name' not in data:
            logger.warning("Name not provided in request")
            return _corsify_actual_response(build_response('fail', 'Name not provided'), 400)

        name = data.get('name', '')
        pig_latin_name = pig_latin(name)
        logger.info(f"Converted name: {name} to Pig Latin: {pig_latin_name}")
        return _corsify_actual_response(build_response('success', 'Conversion successful', {'pig_latin_name': pig_latin_name}), 200)
    except Exception as e:
        logger.error(f"Error during name conversion: {str(e)}")
        return _corsify_actual_response(build_response('error', str(e)), 500)

# CORS Preflight Handler
def _build_cors_preflight_response():
    response = jsonify({'message': 'CORS preflight'})
    response.headers.add('Access-Control-Allow-Origin', 'https://zip-latinate-frontend.onrender.com')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

# CORS Response Handler
def _corsify_actual_response(response, status=200):
    response.headers.add('Access-Control-Allow-Origin', 'https://zip-latinate-frontend.onrender.com')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response, status

if __name__ == '__main__':
    app.run()


