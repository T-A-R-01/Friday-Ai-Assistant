from googlesearch import search
from json import load, dump
from datetime import datetime
from groq import Groq
from dotenv import dotenv_values
import os

env_vars = dotenv_values(".env")

Username = env_vars["Username"]
Assistantname = env_vars["Assistantname"]
GroqAPIKey = env_vars["GroqAPIKey"]

if not GroqAPIKey:
    raise ValueError("GroqAPIKey not found in .env file.")

client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Load chat log safely
chatlog_path = r"Data\ChatLog.json"
if not os.path.exists(chatlog_path):
    with open(chatlog_path, "w") as f:
        dump([], f)

def GoogleSearch(query):
    try:
        results = list(search(query, advanced=True, num_results=5))
    except Exception as e:
        return f"Error while performing search: {str(e)}"

    Answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    Answer += "[end]"
    return Answer

def AnswerModifier(Answer):
    if isinstance(Answer, list):
        Answer = ''.join(Answer)

    lines = str(Answer).splitlines()
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

def Information():
    current_date_time = datetime.now()
    return (
        "Use This real-time Information if needed:\n"
        f"Day: {current_date_time.strftime('%A')}\n"
        f"Date: {current_date_time.strftime('%d')}\n"
        f"Month: {current_date_time.strftime('%B')}\n"
        f"Year: {current_date_time.strftime('%Y')}\n"
        f"Time: {current_date_time.strftime('%H')} hours, "
        f"{current_date_time.strftime('%M')} minutes, "
        f"{current_date_time.strftime('%S')} seconds.\n"
    )

def clean_invalid_roles(messages):
    valid_roles = {"system", "user", "assistant"}
    return [msg for msg in messages if msg.get("role") in valid_roles]

def RealtimeSearchEngine(prompt):
    global SystemChatBot

    with open(chatlog_path, "r") as f:
        messages = load(f)

    messages = clean_invalid_roles(messages)  # Clean invalid messages
    messages.append({"role": "user", "content": prompt})

    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    with open(chatlog_path, "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()

    return AnswerModifier(Answer=Answer)

# ✅ Main Entry Point
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))