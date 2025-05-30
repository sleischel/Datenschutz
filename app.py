from flask import Flask, render_template, request, redirect, url_for, session
import json
import random
import re  # für Normalisierung

app = Flask(__name__)
app.secret_key = "supergeheim"  # In Produktion sicher setzen!

# Fragen aus JSON laden
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Hilfsfunktion zur Normalisierung von Antworten
def normalize_answer(ans):
    return re.sub(r"[^\wäöüß]", "", ans.lower().strip())

# Startseite
@app.route("/")
def quiz_start():
    return render_template("quiz.html")

# Fragenlogik
@app.route("/questions/<int:qid>", methods=["GET", "POST"])
def questions_route(qid):
    if "score" not in session:
        session["score"] = 0
        session["order"] = list(range(len(questions)))
        random.shuffle(session["order"])

    if qid >= len(questions):
        return redirect(url_for("done"))

    current_index = session["order"][qid]
    question_data = questions[current_index]
    feedback = None

    if request.method == "POST":
        user_answer = request.form.get("answer", "")
        normalized_user_answer = normalize_answer(user_answer)
        correct_answers = [normalize_answer(ans) for ans in question_data["answers"]]

        if normalized_user_answer in correct_answers:
            feedback = "✅ Richtig!"
            session["score"] += 1
        else:
            feedback = "❌ Falsch."

        return render_template(
            "questions.html",
            question=question_data["question"],
            feedback=feedback,
            explanation=question_data.get("explanation", ""),
            qid=qid,
            next_qid=qid + 1,
            total=len(questions),
            score=session["score"]
        )

    return render_template(
        "questions.html",
        question=question_data["question"],
        feedback=None,
        explanation=question_data.get("explanation", ""),
        qid=qid,
        next_qid=qid + 1,
        total=len(questions),
        score=session["score"]
    )

# Abschlussseite
@app.route("/done")
def done():
    return render_template("done.html", score=session.get("score", 0), total=len(questions))

# Quiz zurücksetzen
@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("quiz_start"))

# Datenschutzerklärung
@app.route("/datenschutz")
def datenschutz():
    return render_template("datenschutz.html")

# Impressum
@app.route("/impressum")
def impressum():
    return render_template("impressum.html")

# App starten
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
