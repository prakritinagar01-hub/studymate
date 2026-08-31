function showSection(sectionId) {

    const sections = document.querySelectorAll(".section");

    sections.forEach(section => {
        section.classList.add("hidden");
    });

    document
        .getElementById(sectionId)
        .classList.remove("hidden");
}


// STUDY PLAN

async function generatePlan() {

    const subjects = document.getElementById("subjects").value;
    const hours = document.getElementById("hours").value;
    const examDate = document.getElementById("examDate").value;

    const result = document.getElementById("planResult");

    result.innerHTML = "Generating plan...";

    const response = await fetch("/api/plan", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            subjects: subjects,
            hours: hours,
            exam_date: examDate
        })
    });

    const data = await response.json();

    result.innerHTML =
        `<pre>${data.result}</pre>`;
}


// QUIZ
```javascript
async function generateQuiz() {

    const topic = document
        .getElementById("quizTopic")
        .value
        .trim();

    const difficulty = document
        .getElementById("difficulty")
        .value;

    const result = document
        .getElementById("quizResult");

    if (!topic) {
        result.innerHTML = "Please enter a topic first.";
        return;
    }

    result.innerHTML = "Generating quiz...";

    try {

        const response = await fetch("/api/quiz", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                topic: topic,
                difficulty: difficulty
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.result || "Something went wrong");
        }

        result.innerHTML =
            `<pre>${data.result}</pre>`;

    } catch (error) {

        console.error("Quiz Error:", error);

        result.innerHTML =
            <p>❌ ${error.message}</p>;
    }
}
```


// SUMMARIZER

async function summarizeNotes() {

    const notes =
        document.getElementById("notesInput").value;

    const result =
        document.getElementById("summaryResult");

    result.innerHTML = "Summarizing...";

    const response = await fetch("/api/summarize", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            notes: notes
        })
    });

    const data = await response.json();

    result.innerHTML =
        `<pre>${data.result}</pre>`;
}


// PROGRESS

async function saveProgress() {

    const subject =
        document.getElementById("progressSubject").value;

    const topic =
        document.getElementById("progressTopic").value;

    await fetch("/api/progress", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            subject: subject,
            topic: topic,
            completed: 1
        })
    });

    loadProgress();
}


async function loadProgress() {

    const response =
        await fetch("/api/progress");

    const data =
        await response.json();

    const result =
        document.getElementById("progressResult");

    result.innerHTML = "";

    data.forEach(item => {

        const div =
            document.createElement("div");

        div.className = "progress-item";

        div.innerHTML =
            `✓ ${item.subject} — ${item.topic}`;

        result.appendChild(div);
    });
}


// POMODORO

let time = 25 * 60;
let timer = null;


function updateTimer() {

    const minutes =
        Math.floor(time / 60);

    const seconds =
        time % 60;

    document.getElementById("timer")
        .innerText =
        `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}


function startTimer() {

    if (timer !== null)
        return;

    timer = setInterval(() => {

        if (time <= 0) {

            clearInterval(timer);
            timer = null;

            alert("Pomodoro session completed!");

            return;
        }

        time--;

        updateTimer();

    }, 1000);
}


function resetTimer() {

    clearInterval(timer);

    timer = null;

    time = 25 * 60;

    updateTimer();
}


loadProgress();
updateTimer();