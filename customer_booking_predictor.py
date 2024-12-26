# -*- coding: utf-8 -*-
"""customer booking predictor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zqVBDgLpQgNU_DCpqYwnRXH_MygHi3zE
"""

#pip install streamlit

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

@st.cache
def load_data():
    # Use the raw URL to access the CSV data directly
    url = "https://raw.githubusercontent.com/xbabs/Customer-Buying-Behaviour-Prediction---British-Airways/main/BA%20customer_booking.csv"

    # Try different delimiters if necessary
    # data = pd.read_csv(url, sep=';')  # Example with semicolon delimiter

    # Explicitly specify the encoding as 'latin-1'
    data = pd.read_csv(url, encoding='latin-1')  # Or 'ISO-8859-1'
    return data

data = load_data()
data.head()

# App title
st.title("British Airways Customer Booking Prediction")
data = load_data()

# Display raw dataset
st.subheader("Dataset Overview")
st.write(data.head())
st.write(f"Shape of dataset: {data.shape}")

# Preprocessing
st.subheader("Data Preprocessing")
data['flight_day'] = data['flight_day'].map({"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6, "Sun": 7})
data.fillna(0, inplace=True)
st.write("Data cleaned. Sample:")
st.write(data.head())

# Feature Selection
X = data.drop(columns=['booking_complete'])
y = data['booking_complete']
X = pd.get_dummies(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model selection
st.subheader("Model Selection and Training")
model_name = st.selectbox("Choose a model to train:", [
    "Random Forest",
    "Logistic Regression",
    "Decision Tree",
    "Support Vector Machine",
    "K-Nearest Neighbors",
    "Naive Bayes"
])

# Model dictionary
models = {
    "Random Forest": RandomForestClassifier(random_state=42),
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(),
    "Support Vector Machine": SVC(probability=True),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Naive Bayes": GaussianNB()
}

# Train selected model
model = models[model_name]
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob) if y_prob is not None else "N/A"
st.write(f"**Accuracy:** {accuracy:.2f}")
st.write(f"**ROC AUC:** {roc_auc}")

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
st.write("**Confusion Matrix:**")
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues")
st.pyplot()

# Feature Importance (if applicable)
if hasattr(model, 'feature_importances_'):
    st.subheader("Feature Importance")
    feature_importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    st.bar_chart(feature_importance.head(10))

# Make predictions
st.subheader("Make a Prediction")
input_data = {}
for col in X.columns:
    input_data[col] = st.number_input(f"{col}", value=0)

# Convert input to DataFrame
input_df = pd.DataFrame([input_data])
if st.button("Predict Booking Completion"):
    prediction = model.predict(input_df)
    result = "Booking Completed" if prediction[0] == 1 else "Booking Not Completed"
    st.success(f"Prediction: {result}")

