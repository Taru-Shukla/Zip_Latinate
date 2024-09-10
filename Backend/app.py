from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this in production

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class SavedSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(5), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    population = db.Column(db.Integer, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

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

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    print(f"Attempting login for username: {username}")  # Log the username
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        print("Password matches")  # Log successful password match
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    else:
        print("Invalid credentials")  # Log invalid credentials
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/save_search', methods=['POST'])
@jwt_required()
def save_search():
    current_user = get_jwt_identity()
    data = request.get_json()
    name = data['name']
    zip_code = data['zip_code']
    county = data['county']
    population = data['population']

    new_search = SavedSearch(user_id=current_user, name=name, zip_code=zip_code, county=county, population=population)
    db.session.add(new_search)
    db.session.commit()

    return jsonify({"message": "Search saved successfully"}), 201

@app.route('/get_searches', methods=['GET'])
@jwt_required()
def get_saved_searches():
    current_user = get_jwt_identity()
    searches = SavedSearch.query.filter_by(user_id=current_user).all()
    return jsonify([{
        "id": search.id,
        "name": search.name,
        "zip_code": search.zip_code,
        "county": search.county,
        "population": search.population
    } for search in searches]), 200

@app.route('/delete_search/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_search(id):
    current_user = get_jwt_identity()
    search = SavedSearch.query.filter_by(id=id, user_id=current_user).first()

    if search:
        db.session.delete(search)
        db.session.commit()
        return jsonify({"message": "Search deleted successfully"}), 200
    else:
        return jsonify({"error": "Search not found"}), 404

@app.route('/convert_name', methods=['POST'])
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

@app.route('/zipcode_info', methods=['POST'])
def zipcode_info():
    try:
        data = request.get_json()  # Get JSON data
        if not data or 'zip_code' not in data:
            return make_cors_response(jsonify({'error': 'Zip code not provided'}), 400)

        zipcode = data.get('zip_code', '').zfill(5)  # Ensure zip code is 5 digits
        info = zip_code_pop(zipcode)
        if info:
            # Include population in the response
            response = jsonify({
                "county": info['county'],
                "latitude": info['latitude'],
                "longitude": info['longitude'],
                "population": info['population']
            })
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
    app.run()
