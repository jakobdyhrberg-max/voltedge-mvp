import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

data = pd.DataFrame([
    [42, 3.7, 230, 16, 0],
    [48, 4.5, 228, 20, 0],
    [65, 6.5, 232, 25, 0],
    [78, 5.8, 235, 25, 1],
    [95, 1.1, 210, 5, 1],
    [20, 0.0, 0, 0, 1],
    [110, 7.2, 240, 32, 1],
    [39, 4.1, 229, 18, 0],
    [67, 3.0, 198, 15, 1],
    [72, 6.4, 232, 28, 0],
], columns=["temperature", "power", "voltage", "current", "failure"])

X = data[["temperature", "power", "voltage", "current"]]
y = data["failure"]

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "app/ml/maintenance_model.pkl")

predictions = model.predict(X)
print("Model accuracy:", accuracy_score(y, predictions))