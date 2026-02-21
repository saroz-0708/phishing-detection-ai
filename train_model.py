import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample dataset (for testing)
data = {
    "text": [
        "http://secure-paypal-login.com",
        "http://free-facebook-login.net",
        "https://google.com",
        "https://github.com"
    ],
    "label": [1, 1, 0, 0]
}

df = pd.DataFrame(data)

X = df["text"]
y = df["label"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

# Save trained model
joblib.dump(model, "model/phishing_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("✅ Model trained and saved successfully")