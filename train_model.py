import pandas as pd
import re
import joblib

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


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


data = [
    ["12345", "Weak"],
    ["password", "Weak"],
    ["admin123", "Weak"],
    ["qwerty123", "Weak"],
    ["abc12345", "Weak"],
    ["11111111", "Weak"],
    ["password123", "Weak"],
    ["iloveyou", "Weak"],
    ["batangas123", "Weak"],
    ["student123", "Weak"],
    ["123456789", "Weak"],
    ["letmein", "Weak"],
    ["welcome123", "Weak"],

    ["Hello123", "Medium"],
    ["Student2026", "Medium"],
    ["BatStateU123", "Medium"],
    ["MyPass2026", "Medium"],
    ["Computer123", "Medium"],
    ["Nasugbu2026", "Medium"],
    ["College2026", "Medium"],
    ["CicsStudent1", "Medium"],
    ["Project2026", "Medium"],
    ["Docker1234", "Medium"],
    ["Jhayvic2026", "Medium"],
    ["KierAndrei12", "Medium"],
    ["Saipoden2026", "Medium"],

    ["B@tStateU2026!", "Strong"],
    ["Myp@ssW0rd#2026", "Strong"],
    ["C1cs@Nasugbu2026!", "Strong"],
    ["Secur3P@ssword!", "Strong"],
    ["D0ckerK8s@2026!", "Strong"],
    ["Str0ng#Pass2026", "Strong"],
    ["Kubern3tes@App!", "Strong"],
    ["Cyb3rSecurity#1", "Strong"],
    ["P@sswordChecker2026!", "Strong"],
    ["MachineL3arning@123!", "Strong"],
    ["B@ntoBugtongCatibog#2026", "Strong"],
    ["Cl0udN@tiveSecurity!", "Strong"],
    ["D3ployWithK8s@2026", "Strong"]
]

df = pd.DataFrame(data, columns=["password", "strength"])

X = [extract_features(password) for password in df["password"]]
y = df["strength"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

joblib.dump(model, "password_model.pkl")
print("Model saved as password_model.pkl")