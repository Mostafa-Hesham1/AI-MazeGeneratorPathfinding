import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

iris_df = pd.read_csv('Iris.csv')

X = iris_df[['PetalLengthCm', 'PetalWidthCm', 'SepalLengthCm', 'SepalWidthCm']].values
Y = iris_df['Species'].values

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, Y_train)

rf_predictions = rf_classifier.predict(X_test)

rf_accuracy = accuracy_score(Y_test, rf_predictions)
rf_conf_matrix = confusion_matrix(Y_test, rf_predictions)
rf_classification_rep = classification_report(Y_test, rf_predictions)

print("Random Forest Classifier:")
print(f"Accuracy: {rf_accuracy:.2%}")
print("Confusion Matrix:")
print(rf_conf_matrix)
print("Classification Report:")
print(rf_classification_rep)