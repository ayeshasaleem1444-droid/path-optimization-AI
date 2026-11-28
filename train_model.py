import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("lahore_trips.csv")
print(df.shape)

df = pd.get_dummies(df, columns=["vehicle"])

X = df.drop(columns=["actual_duration_min"])
y = df["actual_duration_min"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Train:", X_train.shape)
print("Test:", X_test.shape)
print(X.head())
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
print("Model MAE:", round(mae, 2), "minutes")
print("Model R2:", round(r2, 3))

osrm_mae = mean_absolute_error(y_test, X_test["osrm_duration_min"])
print("OSRM baseline MAE:", round(osrm_mae, 2), "minutes")

joblib.dump(model, "travel_model.pkl")
print("Model saved")
