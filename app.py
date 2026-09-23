from flask import Flask, render_template, request

app = Flask(__name__)

tasks = []

@app.route("/")
def home():
    return render_template("index.html", tasks=tasks)


@app.route("/add-task", methods=["POST"])
def add_task():
    subject = request.form["subject"]
    date = request.form["date"]
    time = request.form["time"]

    tasks.append({
        "subject": subject,
        "date": date,
        "time": time
    })

    return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)