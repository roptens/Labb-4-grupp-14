import json
from flask import Flask, request, jsonify


app = Flask(__name__)


FILE = "cars.json"


#  Läser alla bilar från JSON med json.load
def read_cars():
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# Sparar alla bilar till JSON med json.dump
def write_cars(cars):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=2)


#  Gör registreringsnummer lika varje gång tar bort mellanslag och stora bokstäver
def norm_regnr(regnr):
    return regnr.replace(" ", "").upper().strip()


# start sidan där det finns inget nu men vi kan se om api fungerar eller inte så länge
@app.get("/")
def home():
    return jsonify({"message": "Cars API running"})


#  GET /cars för att hämtar alla bilar
@app.get("/cars")
def get_cars():
    return jsonify(read_cars())


# 🔹 GET /cars/regnr för att hämtar en bil via registreringsnummer
@app.get("/cars/<regnr>")
def get_car(regnr):
    cars = read_cars()
    regnr = norm_regnr(regnr)

    for car in cars:
        if norm_regnr(car["regnr"]) == regnr:
            return jsonify(car)

    # medelande om bilen inte finns
    return jsonify({"error": "Car not found"}), 404


# 🔹 POST /cars för att lägga en ny bil i listan 
@app.post("/cars")
def add_car():
    cars = read_cars()
    data = request.get_json()

    # Kontrollera att JSON skickas och att regnr finns
    if not data or "regnr" not in data:
        return jsonify({"error": "Skicka JSON med regnr"}), 400

    regnr = norm_regnr(data["regnr"])

    # Kontrollera att regnr är unikt
    for car in cars:
        if norm_regnr(car["regnr"]) == regnr:
            return jsonify({"error": "Regnr finns redan"}), 409

    # Skapa en ny bil
    new_car = {
        "regnr": regnr,
        "brand": data.get("brand", ""),
        "model": data.get("model", ""),
        "year": data.get("year", "")
    }

    cars.append(new_car)   # Lägg till bilen i listan med append asså sisty ner i listan
    write_cars(cars)       # Spara  

    return jsonify(new_car), 201


#  PUT /cars/regnr för att uppdaterar en bil tillexempel byt namnet
@app.put("/cars/<regnr>")
def update_car(regnr):
    cars = read_cars()
    regnr = norm_regnr(regnr)
    data = request.get_json()

    # Kontrollera att JSON skickas
    if not data:
        return jsonify({"error": "Skicka JSON"}), 400

    for car in cars:
        if norm_regnr(car["regnr"]) == regnr:

            # Uppdatera bara det som skickas
            if "brand" in data:
                car["brand"] = data["brand"]
            if "model" in data:
                car["model"] = data["model"]
            if "year" in data:
                car["year"] = data["year"]

            write_cars(cars)  # Spara ändringar
            return jsonify(car)

    return jsonify({"error": "Car not found"}), 404


# DELETE /cars/regnr tar bort en bil
@app.delete("/cars/<regnr>")
def delete_car(regnr):
    cars = read_cars()
    regnr = norm_regnr(regnr)

    for i, car in enumerate(cars):
        if norm_regnr(car["regnr"]) == regnr:
            deleted = cars.pop(i)  # Ta bort bilen från listan
            write_cars(cars)       # Spara 
            return jsonify({"message": "Deleted", "car": deleted}) #medlande när bilen tas bort

    return jsonify({"error": "Car not found"}), 404



if __name__ == "__main__":
    app.run(debug=True)
