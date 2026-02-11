from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

client = Groq(
    api_key="api_key"
)

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""

    if request.method == "POST":
        user_input = request.form["question"]
        action = request.form["action"]

        if action == "explain":
            prompt = f"Explain this topic in very simple words with examples:\n{user_input}"

        elif action == "quiz":
            prompt = f"""
            Create 5 multiple choice questions (MCQs) on the topic: {user_input}.
            Each question should have 4 options (A, B, C, D).
            Clearly mention the correct answer after each question.
            """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant"
        )

        response_text = chat_completion.choices[0].message.content

    return render_template("index.html", response=response_text)


if __name__ == "__main__":
    app.run(debug=True)
