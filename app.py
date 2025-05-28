import json
import difflib

# Funktion: Tolerante Antwortprüfung
def is_correct(user_input, valid_answers):
    user_input = user_input.lower().strip()
    for answer in valid_answers:
        if difflib.SequenceMatcher(None, user_input, answer).ratio() > 0.8:
            return True
    return False

# Funktion: Quiz durchführen
def run_quiz(questions):
    print("🔐 DSGVO-Quiz gestartet! Bitte beantworte die folgenden Fragen:\n")
    for idx, q in enumerate(questions, start=1):
        print(f"❓ Frage {idx}: {q['question']}")
        user_input = input("📝 Deine Antwort: ")
        if is_correct(user_input, q["answers"]):
            print("✅ Richtig!")
        else:
            print("❌ Leider falsch.")
        print("📘 Richtige Antwort(en):", ", ".join(q["answers"]))
        print("📖 Erläuterung:", q["explanation"])
        print("-" * 60)

# JSON-Datei laden
def load_questions_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print("Fehler beim Laden der Datei:", e)
        return []

# Hauptprogramm
if __name__ == "__main__":
    questions = load_questions_from_file("questions.json")
    if questions:
        run_quiz(questions)
    else:
        print("Keine Fragen gefunden.")
