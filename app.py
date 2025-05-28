from flask import Flask, render_template, request, redirect, url_for
import json
import difflib
import os

app = Flask(__name__)

# Fragen laden mit Fehlerprüfung und Logging
def load_questions():
    import os
    print("📁 Aktuelles Verzeichnis:", os.getcwd())
    print("🔍 Existiert questions.json?", os.path.exists("questions.json"))

    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
            print(f"✅ {len(questions)} Fragen erfolgreich geladen.")
            return questions
    except Exception as e:
        print(f"❌ Fehler beim Laden der Fragen: {e}")
        return []

questions = load_questions()
print(f"❗ Geladene Fragen: {questions}")

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
                       correct_answers=correct_answers, explanation=explanation, total=len(questions))

@app.route("/next/<int:qid>")
def next_question(qid):
    return redirect(url_for("question", qid=qid + 1))
    
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Nutze Umgebungsvariable oder Standard-Port 5000
    app.run(host="0.0.0.0", port=port)
