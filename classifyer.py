import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE


data = pd.read_csv("data_versions/labelled.csv")
job_descriptions = data["description"]
labels = data["label"]

tfidf_vectorizer = TfidfVectorizer(max_features=1000)
X = tfidf_vectorizer.fit_transform(job_descriptions)

# Oversampling to balance the dataset because 0 is much more common than 1. (0 being realistic and 1 being unrealistic)
smote = SMOTE(sampling_strategy='minority', random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, labels)
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=40)

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
}

model = GradientBoostingClassifier(random_state=42)
grid_search = GridSearchCV(model, param_grid, cv=3, n_jobs=-1)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
print(best_model)
best_model.fit(X_train, y_train)

# Predictions
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("Best Hyperparameters:", grid_search.best_params_)
print(f"Accuracy: {accuracy}")
print(report)

# Save the best model
# model_filename = "best_model.pkl"
# joblib.dump(best_model, model_filename)
