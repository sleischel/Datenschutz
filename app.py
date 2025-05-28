from flask import Flask, render_template, request, redirect, url_for
import json
import difflib

app = Flask(__name__)

# Fragen laden
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

# Toleranter Antwortvergleich
def is_correct(user_input, valid_answers):
    user_input = user_input.lower().strip()
    for answer in valid_answers:
        if difflib.SequenceMatcher(None, user_input, answer).ratio() > 0.8:
            return True
    return False

@app.route("/")
def index():
    return redirect(url_for("question", qid=0))

@app.route("/question/<int:qid>", methods=["GET", "POST"])
def question(qid):
    if qid >= len(questions):
        return render_template("done.html")

    q = questions[qid]
    feedback = None
    explanation = None
    correct_answers = None
    correct = None

    if request.method == "POST":
        user_input = request.form.get("answer", "")
        correct = is_correct(user_input, q["answers"])
        feedback = "✅ Richtig!" if correct else "❌ Leider falsch."
        correct_answers = ", ".join(q["answers"])
        explanation = q["explanation"]

    return render_template("quiz.html", qid=qid, question=q["question"], feedback=feedback,
                           correct_answers=correct_answers, explanation=explanation)

@app.route("/next/<int:qid>")
def next_question(qid):
    return redirect(url_for("question", qid=qid + 1))
    
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Nutze Umgebungsvariable oder Standard-Port 5000
    app.run(host="0.0.0.0", port=port)
