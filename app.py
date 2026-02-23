from flask import Flask, jsonify
from cars.routes import cars_bp  # import blueprinten

app = Flask(__name__)

# registrera blueprint
app.register_blueprint(cars_bp)

@app.get("/")
def home():
    return jsonify({"message": "Cars API running with Blueprint"})

if __name__ == "__main__":
    app.run(debug=True)