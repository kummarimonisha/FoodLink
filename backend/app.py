# simple Flask skeleton for FoodLink backend
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(message="FoodLink backend up")

if __name__ == '__main__':
    app.run(debug=True)
