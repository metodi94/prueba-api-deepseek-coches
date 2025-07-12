from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import json

app = Flask(__name__)

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
coches_collection = db['coches']

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app.json_encoder = JSONEncoder

@app.route('/coches', methods=['GET'])
def get_coches():
    coches = list(coches_collection.find())
    return jsonify(coches), 200

@app.route('/coches/<id>', methods=['GET'])
def get_coche(id):
    coche = coches_collection.find_one({'_id': ObjectId(id)})
    if coche:
        return jsonify(coche), 200
    return jsonify({'error': 'Coche no encontrado'}), 404

@app.route('/coches', methods=['POST'])
def add_coche():
    data = request.json
    required_fields = ['marca', 'modelo', 'anio', 'potencia', 'matricula', 'color']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400
        
    result = coches_collection.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@app.route('/coches/<id>', methods=['PUT'])
def update_coche(id):
    data = request.json
    result = coches_collection.update_one(
        {'_id': ObjectId(id)},
        {'$set': data}
    )
    if result.modified_count:
        return jsonify({'message': 'Coche actualizado'}), 200
    return jsonify({'error': 'Coche no encontrado'}), 404

@app.route('/coches/<id>', methods=['DELETE'])
def delete_coche(id):
    result = coches_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Coche eliminado'}), 200
    return jsonify({'error': 'Coche no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)