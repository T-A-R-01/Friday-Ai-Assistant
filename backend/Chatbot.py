from groq import Groq # importing the groq api to use its library.
from json import load, dump # importing functions to read write json files.
import datetime # importing datetime to get the current date and time.
from dotenv import dotenv_values # importing dotenv to load environment variables from .env file.

# load environment variables from .env file
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get('Username')
Assistantname = env_vars.get('Assistantname')
GroqAPIKey = env_vars.get('GroqAPIKey')

# Initialize the groq client using the provided API key
client = Groq(api_key = GroqAPIKey)

# Initialize an empty list to store chat messages.
messages = []

# Define a system message that provides context to the AI chatbot about its role and behaviour.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# A list of system instructions for the chatbot.
SystemChatBot = [
    {"role": "system", "content": System}
]

# Attempt to load the chat history from a JSON file.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)   # load exixting chat history from the log.
except FileNotFoundError:
    #if the file is not found, create a new file.
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
        
# Function to get real-time date and time information.
def RealtimeInformation():
    # Get the current date and time.
    current_date_time = datetime.datetime.now()

    day = current_date_time.strftime("%A")  # Get the day of the week.
    date = current_date_time.strftime("%d")  # Get the date.
    month = current_date_time.strftime("%B")  # Get the month.
    year = current_date_time.strftime("%Y")  # Get the year.
    hour = current_date_time.strftime("%H")  # Get the hour.
    minute = current_date_time.strftime("%M")  # Get the minute.
    second = current_date_time.strftime("%S")  # Get the second.
    
    # Format the date and time information.
    data = f"please use this realtime information if needed.\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours: {minute} minutes: {second} seconds.\n"
    return data

# Function to modify chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split('\n')  # Split the response into lines.
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines.
    modified_answer = '\n'.join(non_empty_lines)  # Join the non-empty lines.
    return modified_answer

# Main Chatbot function to handle user queries.

def ChatBot(Query):
    '''This function sends the user query to the groq api and returns the response.'''
    try:
        # load existing chatlog from json file.
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
            
        # Append the users query to the message list.
        messages.append({"role": "user", "content": f"{Query}"})
        
        # Make a request to the groq api for a response.
        completion = client.chat.completions.create(
            model = "llama3-70b-8192", # specify the ai model to use.
            messages = SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages, # include system infomation, real-time information , chat history.
            max_tokens = 1024, # limit the maximum token in the response.
            temperature = 0.7, # Adjust response randomness. (higher means more)
            top_p = 1,  # Use nucleus sampling to control diversity.
            stream = True,  #Enable streaming response.
            stop = None,  # Allow the model to determine when to stop.
        )
        
        # Initialize an empty string to store the generated response.
        Answer = ""
        
        # Process the streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:    # Check if there's content in the current chunk.
                Answer += chunk.choices[0].delta.content     #Append the content to the answer.
                
        Answer = Answer.replace("</s>", "")  # Clenip any unwanted tokens from the response.
        
        # Append the chatbot's response to the message list.
        messages.append({"role": "assistant", "content": f"{Answer}"})
        
        # save the updated chatlog to the json file.
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent = 4)
            
        # Return the formatted response.
        return AnswerModifier(Answer=Answer)
    
    except Exception as e:
        # handle the error by printing the exceptions and resetting chatlog.
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:     
            dump([], f, indent = 4)
        return ChatBot(Query)  # Retry the query after resetting the log.
    
    
# Main program entry point.
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")     # Prompt the user for input.
        print(ChatBot(user_input))  # Print the chatbot's response.