from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_user_by_id(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # DANGEROUS: vulnerable to SQL injection!
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

@app.route("/user")
def user():
    user_id = request.args.get("id", "")
    rows = get_user_by_id(user_id)
    if rows:
        return "<br>".join([str(row) for row in rows])
    else:
        return "No user found."

if __name__ == "__main__":
    app.run(debug=True)
