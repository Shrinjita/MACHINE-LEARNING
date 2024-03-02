

from transformers import BertTokenizer

from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM





# Instantiate the ChatGPT model
model = ChatGPT.from_pretrained("facebook/chatbot-gpt-2.0")

# Define a function to generate responses
def generate_response(prompt):
    conversation_history = model.generate_response(prompt)
    return conversation_history.choices[0].message['content']

# Example conversation starter
user_input = "Can you tell me about the company culture?"

# Get chatbot's response
bot_response = generate_response(user_input)

# Print the bot's response
print(bot_response)

from transformers import ConversationSummary
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config, Conversation

# Define your conversational dataset
conversations = [
    Conversation(evidence=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Can you tell me about the company culture?"}
    ]),
    # Add more conversations as needed
]

# Tokenizer and model initialization
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel(GPT2Config.from_pretrained("gpt2"))

# Tokenize the conversations
inputs = tokenizer([conv.to_dict() for conv in conversations], return_tensors="pt", padding=True, truncation=True)

# Fine-tune the model
labels = inputs["input_ids"].clone()
labels[labels == tokenizer.pad_token_id] = -100  # Ignore padding tokens during training

model.train()
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

for epoch in range(3):  # Adjust the number of epochs as needed
    outputs = model(**inputs, labels=labels)
    loss = outputs.loss
    loss.backward()
    optimizer.step()

# Save the fine-tuned model
model.save_pretrained("./fine_tuned_chatbot")

# Now you can load and use the fine-tuned model for generating responses
fine_tuned_model = GPT2LMHeadModel.from_pretrained("./fine_tuned_chatbot")

# Example usage
user_input = "Can you tell me about the company culture?"
input_ids = tokenizer.encode(user_input, return_tensors="pt")
bot_response_ids = fine_tuned_model.generate(input_ids, max_length=50, num_beams=5, no_repeat_ngram_size=2)
bot_response = tokenizer.decode(bot_response_ids[0], skip_special_tokens=True)
print(bot_response)



import json

def load_responses():
    try:
        with open('data1.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_responses(responses):
    with open('responses.json', 'w') as file:
        json.dump(responses, file, indent=2)

def get_response(user_input, responses):
    return responses.get(user_input, "I'm sorry, I don't understand that.")

def train_chatbot(responses):
    print("Training the chatbot. Type 'exit' to stop training.")

    while True:
        user_input = input("You (Type 'exit' to stop training): ")

        if user_input.lower() == 'exit':
            print("Training complete!")
            break

        new_response = input("Chatbot (Provide a response): ")
        responses[user_input.lower()] = new_response

    save_responses(responses)

def main():
    print("Chatbot: Hello! Type 'train' to update responses or 'exit' to end the conversation.")

    responses = load_responses()

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        elif user_input.lower() == 'train':
            train_chatbot(responses)
        else:
            response = get_response(user_input, responses)
            print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()

# prompt: AUTOMATED CHATBOT RUNS ON A DYNAMIC JSON FILE

def load_responses():
    try:
        with open('responses.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_responses(responses):
    with open('responses.json', 'w') as file:
        json.dump(responses, file, indent=2)

def get_response(user_input, responses):
    return responses.get(user_input, "I'm sorry, I don't understand that.")

def train_chatbot(responses):
    print("Training the chatbot. Type 'exit' to stop training.")

    while True:
        user_input = input("You (Type 'exit' to stop training): ")

        if user_input.lower() == 'exit':
            print("Training complete!")
            break

        new_response = input("Chatbot (Provide a response): ")
        responses[user_input.lower()] = new_response

    save_responses(responses)

def main():
    print("Chatbot: Hello! Type 'train' to update responses or 'exit' to end the conversation.")

    responses = load_responses()

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        elif user_input.lower() == 'train':
            train_chatbot(responses)
        else:
            response = get_response(user_input, responses)
            print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()