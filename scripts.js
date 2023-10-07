let currentGrade = null;
let currentQuestionIndex = 0;
let score = 0;
const questions = {
    grade1: [
        { q: "What is 1 + 1?", options: ["1", "2", "3", "4"], correct: 1 },
        { q: "What is 2 + 2?", options: ["2", "3", "4", "5"], correct: 2 }
    ],
    grade2: [
        { q: "What is 2 * 2?", options: ["2", "3", "4", "5"], correct: 2 },
        { q: "What is 3 * 3?", options: ["6", "7", "8", "9"], correct: 3 }
    ],
    algebra: generateAlgebraProblems(),
    quadratic: generateQuadraticProblems()
};

const resources = {
    grade1: [
        { type: 'article', link: 'http://example.com/article-grade1-1', title: 'Understanding Basics of Addition' },
        { type: 'video', link: 'https://youtube.com/xyz-grade1', title: 'Grade 1 Math Basics' }
    ],
    grade2: [
        { type: 'article', link: 'http://example.com/article-grade2-1', title: 'Advanced Grade 2 Math' },
        { type: 'video', link: 'https://youtube.com/xyz-grade2', title: 'Grade 2 Math Mastery' }
    ],
    algebra: [
        { type: 'article', link: 'http://example.com/article-algebra', title: 'Introduction to Algebra' },
        { type: 'video', link: 'https://youtube.com/xyz-algebra', title: 'Algebra Explained' }
    ],
    quadratic: [
        { type: 'article', link: 'http://example.com/article-quadratic', title: 'Understanding Quadratic Equations' },
        { type: 'video', link: 'https://www.youtube.com/watch?v=qeByhTF8WEw&pp=ygUhaG93IHRvIHNvbHZlIHF1YWRyYXRpYyBlcXVhdGlvbnMg', title: 'Quadratic Equation Basics' }
    ]
};




function generateAlgebraProblems() {
    const problems = [];
    
    for (let i = 0; i < 10; i++) {
        let coefficient = Math.floor(Math.random() * 10) + 1;
        let constantTerm = Math.floor(Math.random() * 20) - 10;
        let result = coefficient * (Math.floor(Math.random() * 10) + 1);
        
        let equation = `If ${coefficient}x + ${constantTerm} = ${result + constantTerm}, what is x?`;
        let answer = (result / coefficient).toString();
        
        problems.push({ q: equation, answer: answer });
    }
    
    return problems;
}


function generateQuadraticProblems() {
    const problems = [];
    
    for (let i = 0; i < 10; i++) {
        let a = 1;
        let b = Math.floor(Math.random() * 20) - 10;
        let c = Math.floor(Math.random() * 20) - 10;
        
        let discriminant = b*b - 4*a*c;
        
        if (discriminant >= 0) {
            let root1 = (-b + Math.sqrt(discriminant)) / (2 * a);
            let root2 = (-b - Math.sqrt(discriminant)) / (2 * a);

            let equation = `If the equation is x^2 + ${b}x + ${c} = 0, what are the roots?`;
            let answers = [root1.toFixed(2), root2.toFixed(2)];

            problems.push({ q: equation, answers: answers });
        } else {
            i--;
        }
    }
    
    return problems;
}

function startQuiz() {
    currentGrade = document.getElementById("gradeSelector").value;
    currentQuestionIndex = 0;
    score = 0;
    displayQuestion();
}

function displayQuestion() {
    let questionArea = document.getElementById("questionArea");
    
    if (currentQuestionIndex < questions[currentGrade].length) {
        let currentQuestion = questions[currentGrade][currentQuestionIndex];
    
        let html = `<p>Score: ${score}</p>`;
        html += `<p>${currentQuestion.q}</p>`;
        
        if (currentGrade === "algebra") {
            html += `<input type="text" id="studentAnswer" placeholder="Enter your answer">`;
            html += `<button onclick="checkAnswer('${currentQuestion.answer}')">Submit</button>`;
        } else if (currentGrade === "quadratic") {
            html += `<input type="text" id="studentAnswer1" placeholder="Enter first root">`;
            html += `<input type="text" id="studentAnswer2" placeholder="Enter second root">`;
            html += `<button onclick="checkQuadraticAnswer(['${currentQuestion.answers[0]}', '${currentQuestion.answers[1]}'])">Submit</button>`;
        } else {
            currentQuestion.options.forEach((option, index) => {
                html += `<button onclick="checkMCQAnswer(${index}, ${currentQuestion.correct})">${option}</button>`;
            });
        }

        html += `<p id="feedback"></p>`;
        questionArea.innerHTML = html;
    } else {
        if(score !== questions[currentGrade].length) {
            questionArea.innerHTML = `<p>Quiz finished! Your score is ${score}/${questions[currentGrade].length}. You might want to check out the following resources:</p>`;
            resources[currentGrade].forEach(resource => {
                if(resource.type === 'video') {
                    questionArea.innerHTML += `<a href="${resource.link}" target="_blank"><img src="https://img.youtube.com/vi/${resource.videoId}/0.jpg" alt="${resource.title} thumbnail"><br>${resource.title}</a><br>`;
                } else {
                    questionArea.innerHTML += `<a href="${resource.link}" target="_blank">${resource.title}</a><br>`;
                }
            });
        } else {
            questionArea.innerHTML = `<p>Quiz finished! Your score is ${score}/${questions[currentGrade].length}.</p>`;
        }
    }
}


function checkAnswer(correctAnswer) {
    let studentAnswer = document.getElementById("studentAnswer").value;
    let feedback = document.getElementById("feedback");

    if (studentAnswer === correctAnswer) {
        score++;
        feedback.innerText = "Correct!";
    } else {
        feedback.innerText = `Incorrect. The correct answer is ${correctAnswer}.`;
    }
    setTimeout(() => {
        feedback.innerText = "";
        currentQuestionIndex++;
        displayQuestion();
    }, 2000);
}

function checkQuadraticAnswer(answers) {
    let studentAnswer1 = parseFloat(document.getElementById("studentAnswer1").value).toFixed(2);
    let studentAnswer2 = parseFloat(document.getElementById("studentAnswer2").value).toFixed(2);
    let feedback = document.getElementById("feedback");

    if ((answers.includes(studentAnswer1) && answers.includes(studentAnswer2)) || 
        (answers.includes(studentAnswer2) && answers.includes(studentAnswer1))) {
        score++;
        feedback.innerText = "Correct!";
    } else {
        feedback.innerText = `Incorrect. The correct answers are ${answers[0]} and ${answers[1]}.`;
    }
    setTimeout(() => {
        feedback.innerText = "";
        currentQuestionIndex++;
        displayQuestion();
    }, 2000);
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


