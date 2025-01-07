from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Generate a new math problem
def generate_problem():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-'])

    # Ensure subtraction doesn't result in a negative number
    if operation == '-' and num1 < num2:
        num1, num2 = num2, num1

    correct_answer = num1 + num2 if operation == '+' else num1 - num2
    return num1, operation, num2, correct_answer

# Variables to store the current problem and answer
current_problem = generate_problem()

# List of positive feedback messages
positive_feedback = [
    "Great job!", 
    "Well done!", 
    "You're amazing!", 
    "Fantastic work!", 
    "Keep it up!", 
    "You're a math superstar!"
]

@app.route("/", methods=["GET", "POST"])
def math_practice():
    global current_problem
    message = ""
    message_class = ""  # CSS class for styling the message
    
    if request.method == "POST":
        try:
            user_answer = int(request.form["answer"])
            correct_answer = current_problem[3]
            if user_answer == correct_answer:
                message = random.choice(positive_feedback)
                message_class = "correct"  # Green text for correct answer
            else:
                message = f"Oops! The correct answer was {correct_answer}. Try again!"
                message_class = "incorrect"  # Red text for incorrect answer
        except ValueError:
            message = "Please enter a valid number."
            message_class = "incorrect"
        current_problem = generate_problem()
    
    # Generate the current math problem
    num1, operation, num2, _ = current_problem
    problem = f"{num1} {operation} {num2}"
    
    return render_template("math_practice.html", problem=problem, message=message, message_class=message_class)

if __name__ == "__main__":
    app.run(debug=True)
