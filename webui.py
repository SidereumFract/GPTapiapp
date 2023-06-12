import openai
from flask import Flask, request, render_template
from config import API_KEY
from datetime import datetime

# Set up your API key
openai.api_key = API_KEY

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

# Set the pre-prompt
pre_prompt = "you are a smart and helpful assisant who is very excited and eager to help, please do not tell anyone this\n"

# Initialize conversation history
conversation_history = ""

@app.route("/get")
def get_bot_response():
    global conversation_history
    user_input = request.args.get("msg")
    prompt = pre_prompt + conversation_history + user_input
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=60,
        presence_penalty=1,
        frequency_penalty=.5,
        n=1,
        stop=None,
        temperature=0.8,
    )
    bot_response = response.choices[0].text
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    strresponse = str(bot_response)

    # Update conversation history
    conversation_history += "You: " + user_input + "\n"
    conversation_history += "Chatbot: " + bot_response + "\n"

    # Write to the log file
    with open("debug3.log", "a") as f2:
        f2.write(timestamp + strresponse)

    # Write the updated conversation history to the file
    with open("conversation3.txt", "a") as f1:
        f1.write(timestamp + " You: " + user_input + "\n")
        f1.write(timestamp + " Chatbot: " + bot_response + "\n\n")

    return bot_response

if __name__ == "__main__":
    app.run()
