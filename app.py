from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = "supergeheim"  # In Produktion unbedingt ändern

# Fragen laden
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Startseite (animierte Einführung)
@app.route("/")
def index():
    return redirect(url_for("quiz"))  # ✅ 'quiz' ist der korrekte Funktionsname
    session.clear()
    return render_template("quiz.html")
    
# Fragen-Route
@app.route("/questions/<int:qid>", methods=["GET", "POST"])
def questions_route(qid):
    if "score" not in session:
        session["score"] = 0
        session["order"] = list(range(len(questions)))
        random.shuffle(session["order"])

    # Quiz beendet?
    if qid >= len(questions):
        return redirect(url_for("done"))

    current_index = session["order"][qid]
    question_data = questions[current_index]
    feedback = None

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip().lower()
        correct_answers = [ans.strip().lower() for ans in question_data["answers"]]

        if user_answer in correct_answers:
            feedback = "✅ Richtig!"
            session["score"] += 1
        else:
            feedback = f"❌ Falsch. Richtige Antwort: {question_data['answers'][0]}"

        return render_template(
            "question.html",
            question=question_data["question"],
            feedback=feedback,
            explanation=question_data.get("explanation", ""),
            qid=qid,
            next_qid=qid + 1,
            total=len(questions),
            score=session["score"]
        )

    return render_template(
        "question.html",
        question=question_data["question"],
        feedback=None,
        explanation="",
        qid=qid,
        next_qid=qid,
        total=len(questions),
        score=session["score"]
    )

# Abschlussseite
@app.route("/done")
def done():
    return render_template("done.html", score=session.get("score", 0), total=len(questions))

# Reset-Funktion
@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("start"))

# App starten
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

