from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return '''
        <h2>Comment Form (Safe)</h2>
        <form method="POST" action="/comment">
            Name: <input name="name"><br>
            Comment: <textarea name="comment"></textarea><br>
            <input type="submit">
        </form>
    '''

@app.route("/comment", methods=["POST"])
def comment():
    name = escape(request.form["name"])
    comment = escape(request.form["comment"])
    return render_template("safe.html", name=name, comment=comment)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
