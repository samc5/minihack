let currentGrade = null;
let currentQuestionIndex = 0;
let score = 0;

function startQuiz() {
    currentGrade = document.getElementById("gradeSelector").value;
    currentQuestionIndex = 0;
    score = 0;
    displayQuestion();
}

function displayQuestion() {
    let questionArea = document.getElementById("questionArea");
    
    const questions = {
        grade1: [
            {
                q: "What is 1 + 1?",
                options: ["1", "2", "3", "4"],
                correct: 1
            },
            {
                q: "What is 2 + 2?",
                options: ["2", "3", "4", "5"],
                correct: 2
            }
        ],
        grade2: [
            {
                q: "What is 2 * 2?",
                options: ["2", "3", "4", "5"],
                correct: 2
            },
            {
                q: "What is 3 * 3?",
                options: ["6", "7", "8", "9"],
                correct: 3
            }
        ]
    };
    
    if (currentQuestionIndex < questions[currentGrade].length) {
        let currentQuestion = questions[currentGrade][currentQuestionIndex];
    
        let html = `<p>Score: ${score}</p>`;
        html += `<p>${currentQuestion.q}</p>`;
        currentQuestion.options.forEach((option, index) => {
            html += `<button onclick="checkAnswer(${index}, ${currentQuestion.correct})">${option}</button>`;
        });

        questionArea.innerHTML = html;
    } else {
        questionArea.innerHTML = `<p>Quiz finished! Your score is ${score}/${questions[currentGrade].length}.</p>`;
    }
}

function checkAnswer(selected, correct) {
    if (selected === correct) {
        score++;
    }
    
    currentQuestionIndex++;
    displayQuestion();
}
