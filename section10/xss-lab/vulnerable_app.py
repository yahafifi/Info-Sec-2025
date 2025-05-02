from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    return '''
        <h2>Comment Form (Vulnerable)</h2>
        <form method="POST" action="/comment">
            Name: <input name="name"><br>
            Comment: <textarea name="comment"></textarea><br>
            <input type="submit">
        </form>
    '''

@app.route("/comment", methods=["POST"])
def comment():
    name = request.form["name"]
    comment = request.form["comment"]

    # This renders user input without escaping = vulnerable to XSS!
    return render_template_string(f'''
        <h2>Thank you, {name}</h2>
        <p>Your comment:</p>
        <div>{comment}</div>
        <a href="/">Back</a>
    ''')

if __name__ == "__main__":
    app.run(debug=True)
