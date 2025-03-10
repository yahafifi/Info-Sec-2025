# python -m venv abbasa
# source abbasa/bin/activate
# pip install flask PyJWT
# pip install flask_sqlalchemy pymysql

from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import jwt, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/Lec2_API_Course'
db = SQLAlchemy(app)
SECRET_KEY = "abbasa"

class Items(db.Model):
    __tablename__ = 'Items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name
        }

@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if auth['username'] == "user" and auth['password'] == "pass":
        token = jwt.encode({
            'user': auth['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'error': 'Unauthorized'}), 401


@app.route('/items', methods=['GET'])
def get_items():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        items = Items.query.all()
        return jsonify([item.to_dict() for item in items])
    except:
        return jsonify({'error': 'Invalid or expired token'}), 401    

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        item = Items.query.get(item_id)
        if item is None:
            return abort(404)
        else:
            return jsonify(item.to_dict())
    except:
        return jsonify({'error': 'Invalid or expired token'}), 401
  
    
@app.route('/items', methods=['POST'])
def create_item():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if not request.json or 'name' not in request.json:
            abort(404)
        name = request.json['name']
        new_item = Items(name=name)
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict())
    except:
        return jsonify({'error': 'Invalid or expired token'}), 401
    

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if not request.json or 'name' not in request.json:
            abort(404)
        name = request.json['name']
        item = Items.query.get(item_id)
        if item is None:
            return abort(404)
        item.name = name
        db.session.commit()
        return jsonify(item.to_dict())
    except:
        return jsonify({'error': 'Invalid or expired token'}), 401
    

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        item = Items.query.get(item_id)
        if item is None:
            return abort(404)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'result': True})
    except:
        return jsonify({'error': 'Invalid or expired token'}), 401
    

if __name__ == '__main__':
    app.run(debug=True)
