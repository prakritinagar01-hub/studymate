from flask import Flask, render_template, request, jsonify
import sqlite3
from ai_service import generate_ai_response

app = Flask(__name__)

DB_NAME = "studymate.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/plan", methods=["POST"])
def create_plan():
    data = request.json

    subjects = data.get("subjects", "")
    hours = data.get("hours", "")
    exam_date = data.get("exam_date", "")

    prompt = f"""
    Create a practical study plan for a student.

    Subjects:
    {subjects}

    Available study hours per day:
    {hours}

    Exam date:
    {exam_date}

    Give a day-wise plan with:
    - Subject
    - Topic
    - Duration
    - Revision time
    """

    result = generate_ai_response(prompt)

    return jsonify({"result": result})


@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.json

    notes = data.get("notes", "")

    prompt = f"""
    Summarize the following study notes.

    Give:
    1. Short summary
    2. Important points
    3. Important definitions
    4. Quick revision points

    Notes:
    {notes}
    """

    result = generate_ai_response(prompt)

    return jsonify({"result": result})


@app.route("/api/quiz", methods=["POST"])
def quiz():
    data = request.json

    topic = data.get("topic", "")
    difficulty = data.get("difficulty", "Medium")

    prompt = f"""
    Generate 5 multiple-choice questions.

    Topic: {topic}
    Difficulty: {difficulty}

    For every question provide:
    - Question
    - Four options
    - Correct answer
    - Short explanation
    """

    result = generate_ai_response(prompt)

    return jsonify({"result": result})


@app.route("/api/progress", methods=["GET"])
def progress():
    conn = get_db()

    rows = conn.execute("""
        SELECT * FROM progress
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


```python
@app.route("/api/quiz", methods=["POST"])
def quiz():
    try:
        data = request.get_json()

        topic = data.get("topic", "").strip()
        difficulty = data.get("difficulty", "Medium")

        if not topic:
            return jsonify({
                "result": "Please enter a topic first."
            }), 400

        prompt = f"""
You are an expert educational quiz generator.

Generate exactly 5 multiple-choice questions.

Topic: {topic}
Difficulty: {difficulty}

For each question provide:

Question 1:
[question]

A. [option]
B. [option]
C. [option]
D. [option]

Correct Answer: [A/B/C/D]

Explanation: [short explanation]

Repeat the same format for all 5 questions.

Make sure:
- There are exactly 5 questions.
- Each question has exactly 4 options.
- Only one option is correct.
- The questions are relevant to the topic.
- Difficulty should be {difficulty}.
"""

        result = generate_ai_response(prompt)

        return jsonify({
            "result": result
        })

    except Exception as e:
        print("QUIZ ERROR:", str(e))

        return jsonify({
            "result": f"Quiz generation failed: {str(e)}"
        }), 500



if __name__ == "__main__":
    init_db()
    app.run(debug=True)