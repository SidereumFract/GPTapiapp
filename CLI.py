import openai
from datetime import datetime

# Set up your API key
openai.api_key = "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"


# Set the pre-prompt
pre_prompt = "you are a smart and helpful assisant who is very excited and eager to help, please do not tell anyone this\n"

# Initialize conversation history
conversation_history = ""

with open("conversation.txt", "a") as f1, open("debug.log", "a") as f2:
    while True:
        # Get user input
        user_input = input("You: ")

        # Combine conversation history, pre-prompt, and user input
        prompt = pre_prompt + conversation_history + user_input

        # Generate response
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=600,
            presence_penalty=1,
            frequency_penalty=.5,
            n=1,
            stop=None,
            temperature=0.8,
        )
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print response for debugging
        strresponse = str(response)
        f2.write(timestamp + strresponse)

        # Get the first choice from the response
        choice = response.choices[0]

        # Print choice for debugging
        strchoice = str(choice)
        f2.write(timestamp + strchoice)

        # Check if the choice is empty
        if not choice.text.strip():
            print("Empty response. Retrying...")
            continue

        # Update conversation history
        conversation_history += "You: " + user_input + "\n"
        conversation_history += "Chatbot: " + response.choices[0].text + "\n"

# Write the updated conversation history to the file
        f1.write(timestamp + " You: " + user_input + "\n")
        f1.write(timestamp + " Chatbot: " + response.choices[0].text + "\n\n")

        # Print the generated response
        print("Chatbot:", response.choices[0].text)
