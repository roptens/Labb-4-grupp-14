from flask import Blueprint, request, jsonify
from .services import read_cars, write_cars, norm_regnr

cars_bp = Blueprint("cars", __name__, url_prefix="/cars")


# GET /cars
@cars_bp.get("/")
def get_cars():
    return jsonify(read_cars())


# GET /cars/<regnr>
@cars_bp.get("/<regnr>")
def get_car(regnr):
    cars = read_cars()
    regnr = norm_regnr(regnr)

    for car in cars:
        if norm_regnr(car["regnr"]) == regnr:
            return jsonify(car)

    return jsonify({"error": "Car not found"}), 404


# POST /cars
@cars_bp.post("/")
def add_car():
    cars = read_cars()
    data = request.get_json()

    if not data or "regnr" not in data:
        return jsonify({"error": "Skicka JSON med regnr"}), 400

    regnr = norm_regnr(data["regnr"])

    for car in cars:
        if norm_regnr(car["regnr"]) == regnr:
            return jsonify({"error": "Regnr finns redan"}), 409

    new_car = {
        "regnr": regnr,
        "brand": data.get("brand", ""),
        "model": data.get("model", ""),
        "year": data.get("year", "")
    }

    cars.append(new_car)
    write_cars(cars)

    return jsonify(new_car), 201


# PUT /cars/<regnr>
@cars_bp.put("/<regnr>")
def update_car(regnr):
    cars = read_cars()
    regnr = norm_regnr(regnr)
    data = request.get_json()

    if not data:
        return jsonify({"error": "Skicka JSON"}), 400

    for car in cars:
        if norm_regnr(car["regnr"]) == regnr:
            if "brand" in data:
                car["brand"] = data["brand"]
            if "model" in data:
                car["model"] = data["model"]
            if "year" in data:
                car["year"] = data["year"]

            write_cars(cars)
            return jsonify(car)

    return jsonify({"error": "Car not found"}), 404


# DELETE /cars/<regnr>
@cars_bp.delete("/<regnr>")
def delete_car(regnr):
    cars = read_cars()
    regnr = norm_regnr(regnr)

    for i, car in enumerate(cars):
        if norm_regnr(car["regnr"]) == regnr:
            deleted = cars.pop(i)
            write_cars(cars)
            return jsonify({"message": "Deleted", "car": deleted})

    return jsonify({"error": "Car not found"}), 404