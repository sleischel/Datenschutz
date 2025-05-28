from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Lade Fragen aus JSON-Datei
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

@app.route("/", methods=["GET", "POST"])
def quiz():
    feedback = None
    question = questions[0]  # einfache Version: immer nur erste Frage

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip().lower()
        correct_answer = question["answer"].strip().lower()
        if user_answer in correct_answer or correct_answer in user_answer:
            feedback = "✅ Richtig!"
        else:
            feedback = f"❌ Falsch. Die richtige Antwort ist: {question['answer']}"

    return render_template("index.html", question=question["question"], feedback=feedback)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
