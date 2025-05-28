from flask import Flask, render_template, request, session
import json
import random

app = Flask(__name__)
app.secret_key = "supergeheim"  # → Bitte für Produktivbetrieb sicher wählen

# Fragen laden
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

@app.route("/", methods=["GET", "POST"])
def quiz():
    if "score" not in session:
        session["score"] = 0
        session["question_index"] = 0
        random.shuffle(questions)

    feedback = None
    score = session["score"]
    index = session["question_index"]

    # Wenn alle Fragen durch sind
    if index >= len(questions):
        finished = True
        return render_template("index.html", finished=finished, score=score, total=len(questions))
    
    question = questions[index]

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip().lower()
        correct_answer = question["answer"].strip().lower()

        if user_answer in correct_answer or correct_answer in user_answer:
            feedback = "✅ Richtig!"
            session["score"] += 1
        else:
            feedback = f"❌ Falsch. Richtige Antwort: {question['answer']}"

        session["question_index"] += 1

        return render_template(
            "index.html",
            question=questions[session["question_index"]]
            if session["question_index"] < len(questions)
            else None,
            feedback=feedback,
            score=session["score"],
            total=len(questions),
            finished=session["question_index"] >= len(questions)
        )

    return render_template(
        "index.html",
        question=question["question"],
        feedback=None,
        score=score,
        total=len(questions),
        finished=False
    )

@app.route("/reset")
def reset():
    session.clear()
    return "<p>Quiz zurückgesetzt. <a href='/'>Zurück zum Start</a></p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
