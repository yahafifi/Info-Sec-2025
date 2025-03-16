from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    database='info_mgmt_sec_section5'
)

@app.route('/', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    q = f"SELECT * FROM users WHERE username = '{username}' and password = '{password}';"
    cursor = db.cursor()
    cursor.execute(q)
    user = cursor.fetchall()

    if user:
        return jsonify(user)
    else:
        return jsonify({"Error": "Invalid username or password"})
    

if __name__ == '__main__':
    app.run(debug=True)
