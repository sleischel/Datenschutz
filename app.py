from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = "supergeheim"  # In Produktion ersetzen

# Fragen laden
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Startseite (animiert)
@app.route("/quiz")
def start():
    session.clear()
    return render_template("quiz.html")

# Fragen-Logik
@app.route("/questions/<int:qid>", methods=["GET", "POST"])
def questions_route(qid):
    if "score" not in session:
        session["score"] = 0
        session["order"] = list(range(len(questions)))
        random.shuffle(session["order"])

    feedback = None
    finished = qid >= len(questions)

    if finished:
        return redirect(url_for("done"))

    current_index = session["order"][qid]
    question = questions[current_index]
    score = session["score"]

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip().lower()
        correct_answer = question["answer"].strip().lower()

        if user_answer in correct_answer or correct_answer in user_answer:
            feedback = "✅ Richtig!"
            session["score"] += 1
        else:
            feedback = f"❌ Falsch. Richtige Antwort: {question['answer']}"

        return render_template(
            "question.html",
            question=question["question"],
            feedback=feedback,
            qid=qid,
            total=len(questions),
            score=session["score"]
        )

    return render_template(
        "question.html",
        question=question["question"],
        feedback=None,
        qid=qid,
        total=len(questions),
        score=session["score"]
    )

# Abschlussseite
@app.route("/done")
def done():
    return render_template("done.html", score=session.get("score", 0), total=len(questions))

# Reset-Funktion (optional)
@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("start"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
