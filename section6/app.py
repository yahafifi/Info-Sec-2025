# python -m venv venv
# source venv/bin/activate
# pip install flask PyJWT
# pip install flask_sqlalchemy pymysql

from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import jwt, datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/Task2_Info_Sec'
db = SQLAlchemy(app)
SECRET_KEY = "abbasa"

# -------------------- MODELS --------------------

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Products(db.Model):
    __tablename__ = 'Products'
    pid = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# -------------------- USER AUTH --------------------

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if not data or 'username' not in data or 'password' not in data or 'name' not in data:
        return jsonify({'error': 'Missing data'}), 400

    if Users.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    hashed_pw = generate_password_hash(data['password'])
    new_user = Users(name=data['name'], username=data['username'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    user = Users.query.filter_by(username=auth.get('username')).first()
    if user and check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'user': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'error': 'Unauthorized'}), 401

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = Users.query.get(user_id)
        if not user:
            return abort(404)

        data = request.json
        user.name = data.get('name', user.name)
        user.username = data.get('username', user.username)
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    except:
        return jsonify({'error': 'Invalid or expired token'}), 401

# -------------------- PRODUCT ROUTES --------------------

@app.route('/products', methods=['POST'])
def create_product():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        data = request.json
        if not data or 'pname' not in data or 'price' not in data or 'stock' not in data:
            return jsonify({'error': 'Missing fields'}), 400

        new_product = Products(
            pname=data['pname'],
            description=data.get('description'),
            price=data['price'],
            stock=data['stock']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    except:
        return jsonify({'error': 'Invalid or expired token'}), 401

@app.route('/products', methods=['GET'])
def get_products():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        products = Products.query.all()
        result = []
        for p in products:
            result.append({
                'pid': p.pid,
                'pname': p.pname,
                'description': p.description,
                'price': float(p.price),
                'stock': p.stock,
                'created_at': p.created_at.isoformat()
            })
        return jsonify(result)
    except:
        return jsonify({'error': 'Invalid or expired token'}), 401

@app.route('/products/<int:pid>', methods=['GET'])
def get_product(pid):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        product = Products.query.get(pid)
        if not product:
            return abort(404)
        return jsonify({
            'pid': product.pid,
            'pname': product.pname,
            'description': product.description,
            'price': float(product.price),
            'stock': product.stock,
            'created_at': product.created_at.isoformat()
        })
    except:
        return jsonify({'error': 'Invalid or expired token'}), 401

@app.route('/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        product = Products.query.get(pid)
        if not product:
            return abort(404)

        data = request.json
        product.pname = data.get('pname', product.pname)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.stock = data.get('stock', product.stock)
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})
    except:
        return jsonify({'error': 'Invalid or expired token'}), 401

@app.route('/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        product = Products.query.get(pid)
        if not product:
            return abort(404)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    except:
        return jsonify({'error': 'Invalid or expired token'}), 401

# -------------------- MAIN --------------------

if __name__ == '__main__':
    app.run(debug=True)
