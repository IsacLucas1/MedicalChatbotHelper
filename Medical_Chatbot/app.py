from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load predefined responses from a JSON file for symptom chatbot
def load_responses():
    try:
        with open('responses.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

responses = load_responses()

# Route for main page (index.html)
@app.route("/")
def index():
    return render_template("index.html")

# Route for chatbot interaction
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower()  # Make message lowercase for easy matching

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Check if a response exists for the user's message
    response_message = responses.get(user_message, "Sorry, I don't understand that.")

    return jsonify({"response": response_message})

# Route for daily water intake calculation
@app.route("/calculate_water_intake", methods=["POST"])
def calculate_water_intake():
    data = request.json
    age = data.get("age")
    weight = data.get("weight")
    height = data.get("height")
    gender = data.get("gender")
    activity_level = data.get("activity_level")

    if not all([age, weight, height, gender, activity_level]):
        return jsonify({"error": "All fields are required."}), 400

    # Calculate water intake based on the formula:
    water_intake = 0

    # Basic formula based on gender and weight
    if gender == "male":
        water_intake = weight * 35  # 35 ml per kg for men
    else:
        water_intake = weight * 31  # 31 ml per kg for women

    # Adjust for age and activity level
    if age < 18:
        water_intake *= 0.8  # Decrease intake for younger individuals

    if activity_level == "sedentary":
        water_intake *= 1.0
    elif activity_level == "lightly-active":
        water_intake *= 1.2
    elif activity_level == "moderately-active":
        water_intake *= 1.4
    elif activity_level == "very-active":
        water_intake *= 1.6
    elif activity_level == "extremely-active":
        water_intake *= 1.8

    # Convert to liters
    water_intake_liters = water_intake / 1000  # in liters

    return jsonify({"water_intake": f"{water_intake_liters:.2f} liters per day"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
