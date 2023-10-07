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
            { q: "What is 1 + 1?", options: ["1", "2", "3", "4"], correct: 1 },
            { q: "What is 2 + 2?", options: ["2", "3", "4", "5"], correct: 2 }
        ],
        grade2: [
            { q: "What is 2 * 2?", options: ["2", "3", "4", "5"], correct: 2 },
            { q: "What is 3 * 3?", options: ["6", "7", "8", "9"], correct: 3 }
        ],
        algebra: [
            { q: "If x + 2 = 5, what is x?", answer: "3" },
            { q: "If 2x = 10, what is x?", answer: "5" },
            { q: "If 3x + 1 = 10, what is x?", answer: "3" },
            { q: "If x/2 = 4, what is x?", answer: "8" }
        ]
    };
    
    if (currentQuestionIndex < questions[currentGrade].length) {
        let currentQuestion = questions[currentGrade][currentQuestionIndex];
    
        let html = `<p>Score: ${score}</p>`;
        html += `<p>${currentQuestion.q}</p>`;
        
        if (currentGrade === "algebra") {
            html += `<input type="text" id="studentAnswer" placeholder="Enter your answer">`;
            html += `<button onclick="checkAnswer('${currentQuestion.answer}')">Submit</button>`;
        } else {
            currentQuestion.options.forEach((option, index) => {
                html += `<button onclick="checkMCQAnswer(${index}, ${currentQuestion.correct})">${option}</button>`;
            });
        }

        html += `<p id="feedback"></p>`;
        questionArea.innerHTML = html;
    } else {
        questionArea.innerHTML = `<p>Quiz finished! Your score is ${score}/${questions[currentGrade].length}.</p>`;
    }
}

function checkAnswer(correctAnswer) {
    let studentAnswer = document.getElementById("studentAnswer").value;
    let feedback = document.getElementById("feedback");

    if (studentAnswer === correctAnswer) {
        score++;
        feedback.innerText = "Correct!";
        setTimeout(() => {
            feedback.innerText = ""; // Clear feedback
            currentQuestionIndex++;
            displayQuestion();
        }, 2000); // A delay to allow the user to read the feedback before moving to the next question.
    } else {
        feedback.innerText = `Incorrect. The correct answer is ${correctAnswer}.`;
        setTimeout(() => {
            feedback.innerText = ""; // Clear feedback
            currentQuestionIndex++;
            displayQuestion();
        }, 2000); // A delay to allow the user to read the feedback before moving to the next question.
    }
}

function checkMCQAnswer(selected, correct) {
    if (selected === correct) {
        score++;
        alert("Correct!");
    } else {
        alert("Incorrect. Try again."); 
        return; 
    }

    currentQuestionIndex++;
    displayQuestion();
}
