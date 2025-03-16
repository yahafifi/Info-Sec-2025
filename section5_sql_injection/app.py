from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    database='info_mgmt_sec_section5'
)

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        q = f"SELECT * FROM users WHERE username = '{username}' and password = '{password}';"
        cursor = db.cursor()
        cursor.execute(q)
        user = cursor.fetchall()
        
        if user:
            return f'<h1 style="color:green;"> Welcome Mr. {username} </h1> <br> <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQucpUHWz6VWTDfpG5y60bh70JPbtsKvd_i1Q&s">'
        else:
            return '<h1 style="color:red;">أنت مين يا ريس؟؟</h1>'
    else:
        return '''
        <form method="post">
            username: <input type="text" name="username">
            password: <input type="password" name="password">
            <input type="submit">
        </form>
    '''
    

if __name__ == '__main__':
    app.run(debug=True)
