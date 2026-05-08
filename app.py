from flask import Flask, render_template, request, jsonify
import joblib
import re
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret-key")

MODEL_PATH = "password_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None


def extract_features(password):
    length = len(password)
    uppercase = sum(1 for char in password if char.isupper())
    lowercase = sum(1 for char in password if char.islower())
    digits = sum(1 for char in password if char.isdigit())
    symbols = sum(1 for char in password if not char.isalnum())

    common_patterns = ["123", "password", "admin", "qwerty", "abc"]
    has_common_pattern = int(
        any(pattern in password.lower() for pattern in common_patterns)
    )

    repeated_chars = int(bool(re.search(r"(.)\1\1", password)))

    return [
        length,
        uppercase,
        lowercase,
        digits,
        symbols,
        has_common_pattern,
        repeated_chars
    ]


def generate_suggestions(password):
    suggestions = []

    if len(password) < 8:
        suggestions.append("Use at least 8 characters.")

    if len(password) < 12:
        suggestions.append("For better security, use 12 or more characters.")

    if not any(char.isupper() for char in password):
        suggestions.append("Add uppercase letters.")

    if not any(char.islower() for char in password):
        suggestions.append("Add lowercase letters.")

    if not any(char.isdigit() for char in password):
        suggestions.append("Add numbers.")

    if not any(not char.isalnum() for char in password):
        suggestions.append("Add special characters such as @, #, $, or !.")

    common_patterns = ["123", "password", "admin", "qwerty", "abc"]
    if any(pattern in password.lower() for pattern in common_patterns):
        suggestions.append("Avoid common words or common patterns.")

    if re.search(r"(.)\1\1", password):
        suggestions.append("Avoid repeated characters such as aaa or 111.")

    if not suggestions:
        suggestions.append("Your password has good complexity.")

    return suggestions


def calculate_score(password):
    score = 0

    if len(password) >= 8:
        score += 20

    if len(password) >= 12:
        score += 20

    if any(char.isupper() for char in password):
        score += 15

    if any(char.islower() for char in password):
        score += 15

    if any(char.isdigit() for char in password):
        score += 15

    if any(not char.isalnum() for char in password):
        score += 15

    common_patterns = ["123", "password", "admin", "qwerty", "abc"]
    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 20

    if re.search(r"(.)\1\1", password):
        score -= 10

    if score < 0:
        score = 0

    if score > 100:
        score = 100

    return score


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    suggestions = []
    error = None
    score = 0

    if request.method == "POST":
        password = request.form.get("password", "")

        if password.strip() == "":
            error = "Please enter a password."
        elif len(password) > 100:
            error = "Password is too long. Maximum allowed length is 100 characters."
        elif model is None:
            error = "Machine Learning model not found. Please run train_model.py first."
        else:
            features = [extract_features(password)]
            result = model.predict(features)[0]
            suggestions = generate_suggestions(password)
            score = calculate_score(password)

    return render_template(
        "index.html",
        result=result,
        suggestions=suggestions,
        error=error,
        score=score
    )


@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.get_json()
    password = data.get("password", "")

    if password.strip() == "":
        return jsonify({
            "error": "Please enter a password."
        }), 400

    if len(password) > 100:
        return jsonify({
            "error": "Password is too long."
        }), 400

    if model is None:
        return jsonify({
            "error": "Machine Learning model not found."
        }), 500

    features = [extract_features(password)]
    result = model.predict(features)[0]
    suggestions = generate_suggestions(password)
    score = calculate_score(password)

    return jsonify({
        "result": result,
        "score": score,
        "suggestions": suggestions
    })


@app.route("/health")
def health():
    return {
        "status": "running",
        "system": "Password Strength Checker"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)