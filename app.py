from flask import Flask, render_template, request
import sqlite3
import joblib

app = Flask(__name__)

model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/scan", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        text = request.form["text"]
        vect = vectorizer.transform([text])
        result = model.predict(vect)[0]
        prediction = "Phishing ⚠️" if result == 1 else "Legitimate ✅"

        conn = sqlite3.connect("database.db")
        conn.execute(
            "INSERT INTO scan_logs (input_text, result) VALUES (?,?)",
            (text, prediction)
        )
        conn.commit()
        conn.close()

    return render_template("index.html", prediction=prediction)

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    logs = conn.execute("SELECT * FROM scan_logs").fetchall()
    conn.close()
    return render_template("dashboard.html", logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)