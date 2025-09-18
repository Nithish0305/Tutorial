from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello, Interns!"

@app.route("/students")
def students():
    return jsonify([
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ])

if __name__ == "__main__":
    app.run(debug=True)
