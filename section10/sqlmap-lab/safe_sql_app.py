from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_user_by_id(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchall()
    conn.close()
    return result

@app.route("/user")
def user():
    try:
        user_id = int(request.args.get("id", ""))
    except ValueError:
        return "Invalid ID format"

    rows = get_user_by_id(user_id)
    if rows:
        return "<br>".join([str(row) for row in rows])
    else:
        return "No user found."

if __name__ == "__main__":
    app.run(debug=True, port=5001)
