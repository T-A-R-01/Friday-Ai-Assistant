from AppOpener import close, open as appopen
from webbrowser import open as webopen #Import web browser functionality.
from pywhatkit import search, playonyt #Import functions for Google search and YouTube playback.
from dotenv import dotenv_values #Import doteny to manage environment variables.
from bs4 import BeautifulSoup #Import BeautifulSoup for parsing HTML content.
from rich import print  # Import rich for styled console output.
from groq import Groq #Import Grog for Al chat functionalities.
import webbrowser #Import webbrowser for opening URLs.
import subprocess #Import subprocess for interacting with the system.
import requests #Import requests for making HTTP requests.
import keyboard #Import keyboard for keyboard-related actions.
import asyncio #Import asyncin for asynchronous programming.
import os #Import os for operating system functionalities. I
import speech_recognition as sr
import psutil
import pyttsx3
import pygetwindow as gw

#Load environment variables from the env file.
env_vars = dotenv_values(".env")
GroqAPIKey =env_vars.get("GroqAPIKey")

#define css classes
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

#Initialize the Grog client with the API key.
client = Groq(api_key="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")

#Predefined professional responses for user interactions.
professional_responses = [
     "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
     "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]
#List to store chatbot messages.
messages = []

#System message to provide contest to the chathor.
SystemChatBot =[{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, application, essays, notes, songs, poems etc."}]

# Function to perform a Google search.
def GoogleSearch(Topic):
    search (Topic) # Use pywhatkit's search function to perform a Google search.
    return True # Indicate success.



# Function to generate content using AI and save it to a file.
def Content (Topic):
    # Nested function to open a file in Notepad.
    def OpenNotepad (File):
        default_text_editor = 'notepad.exe' # Default text editor. I
        subprocess.Popen([default_text_editor, File]) # Open the file in Notepad.
        

# Nested function to generate content using the AI chatbot.
    def ContentWriterAI (prompt):
        messages.append({"role": "user", "content": f"{prompt}"}) # Add the user's prompt to messages.
    
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Specify the AI model.
            messages=SystemChatBot + messages, # Include system instructions and chat history.
            max_tokens=2048, # Limit the maximum tokens in the response.
            temperature=0.7, # Adjust response randomness.
            top_p=1, # Use nucleus sampling for response diversity.
            stream=True, # Enable streaming response. I
            stop=None # Allow the model to determine stopping conditions.
        )
        Answer = " " # Initialize an empty string for the response.
    
        # Process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content: # Check for content in the current chunk.
                Answer += chunk.choices[0].delta.content # Append the content to the answer.
    
        Answer = Answer.replace("</s>", "") # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer}) # Add the AI's response to messages.
        return Answer  
    
    
    Topic: str = Topic.replace("Content", "") # Remove "Content" from the topic.
    ContentByAI = ContentWriterAI(Topic) # Generate content using AI.
    
    # Save the generated content to a text file.
    with open(rf"Data\{Topic. lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI) # Write the content to the file.
        file.close()

    OpenNotepad (rf"Data\{Topic. lower().replace(' ','')}.txt") # Open the file in Notepad.
    return True # Indicate success.
# Content("write a application for sick leave")

# Function to search for a topic on YouTube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" # Construct the Youtube search URL.
    webbrowser.open(Url4Search) # Open the search URL in a web browser.
    return True # Indicate success.


# Function to play a video on YouTube.
def PlayYoutube (query):
    playonyt(query) # Use pywhatkit's playonyt function to play the video.
    return True # Indicate success.
# PlayYoutube("ram siya ram")


# Function to open ap application or a relevant webpage.

# Dictionary of known apps (Add more if needed)
app_paths = {

    # Microsoft Office (adjust if you installed Office elsewhere)
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
}


# Web fallback
web_urls = {
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "chatgpt": "https://chat.openai.com",
    "whatsapp": "https://web.whatsapp.com",
    "spotify": "https://open.spotify.com",
    "telegram": "https://web.telegram.org",
}

# Text-to-speech
engine = pyttsx3.init()

def speak(text):
    print("Friday:", text)
    engine.say(text)
    engine.runAndWait()

# Google search fallback
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        for link in links:
            href = link.get("href")
            if href and "url?q=" in href:
                return href.split("url?q=")[1].split("&")[0]
    return None

# Main app opener
def OpenApp(app_name):
    app_name = app_name.lower().strip().replace(" ", "")

    if app_name in app_paths:
        try:
            subprocess.Popen(app_paths[app_name], shell=True)
            speak(f"Opening {app_name} locally.")
            return
        except FileNotFoundError:
            speak(f"{app_name} not found locally. Trying web version...")

    if app_name in web_urls:
        webbrowser.open(web_urls[app_name])
        speak(f"Opened {app_name} in web browser.")
        return

    speak(f"{app_name} not found. Performing Google search...")
    result = search_google(app_name)

    if result:
        webbrowser.open(result)
        speak(f"Opened {app_name} via Google search.")
    else:
        print(f"Search failed for: {app_name}")
        print(f"Google URL tried: https://www.google.com/search?q={app_name}")
        speak("No valid search results found.")

# Listen for voice commands
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Voice recognition service is unavailable.")
    return None

# Voice-based app opener
def voice_open_app():
    command = listen_for_command()
    if command:
        if "open" in command.lower():
            app_name = command.lower().replace("open", "").strip()
            OpenApp(app_name)
        else:
            speak("Please say something like 'Open Chrome' or 'Open PowerPoint'.")
            
# OpenApp("power point")
# OpenApp("word")

# Function to close an application.
def CloseApp(app_name):
    app_name = app_name.lower().strip().replace(" ", "")
    if "chrome" in app_name:
        return False  # Skip closing Chrome

    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if app_name in proc.info['name'].lower():
                os.kill(proc.info['pid'], 9)  # Force close the process
                speak(f"Closed {app_name} successfully.")
                return True
    except Exception as e:
        print(f"Error: {e}")

    try:
        windows = gw.getWindowsWithTitle(app_name)
        if windows:
            for window in windows:
                window.close()
                speak(f"Closed {app_name} window.")
                return True
    except Exception as e:
        print(f"Error: {e}")
    
    speak(f"Could not close {app_name}. It may not be running.")
    return False

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Voice recognition service is unavailable.")
    return None

def voice_open_app():
    command = listen_for_command()
    if command:
        if "open" in command.lower():
            app_name = command.lower().replace("open", "").strip()
            OpenApp(app_name)
        else:
            speak("Please say something like 'Open Chrome' or 'Open PowerPoint'.")

def voice_close_app():
    command = listen_for_command()
    if command:
        if "close" in command.lower():
            app_name = command.lower().replace("close", "").strip()
            CloseApp(app_name)
        else:
            speak("Please say something like 'Close Notepad' or 'Close PowerPoint'.")
# CloseApp("PowerPoint")

# Function to execute system-level commands.
def System(command):
    
    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute") # Simulate the mute key press.
        
    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume mute") # Simulate the unmute key press,
        
    def volume_up():
        keyboard.press_and_release("volume up") # Simulate the volume up key press.

    # Nesten fonction to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down") # Simulate the volume down key press.
    
    #Еxecute the soprooriace command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    
    return True #Indicate success.

#Asynchronous function to translare and execute user commands.
async def TranslateAndExecute(commands: list[str]):

    funcs = [] #List to store asunchronous tasks.
    
    for command in commands:
        
        if command.startswith("open "): # Handle "open" commands.
            
            if "open it" in command: # Ignore "open it" commands.
                pass
            
            if "open file" == command: # Ignore "open file" commands.
                pass
            
            else:
                fun = asyncio.to_thread (OpenApp, command.removeprefix("open ")) # Schedule app opening.
                funcs.append(fun)
        
        elif command.startswith("general"): # Placeholder for general commands.
            pass

        elif command.startswith("realtime "): # Placeholder for real-time commands.
            pass
        
        elif command.startswith("close"): # Handle "close" commands.
            fun = asyncio.to_thread (CloseApp, command.removeprefix("close")) # Schedule app closing.
            funcs.append(fun)

        elif command.startswith("play "): # Handle "play" commands.
            fun = asyncio.to_thread (PlayYoutube, command.removeprefix("play ")) # Schedule YouTube playback.
            funcs.append(fun) 
            
        elif command.startswith("content"): #Handle "content" commands.
            fun = asyncio.to_thread (Content, command.removeprefix("content")) # Schedule content creation.
            funcs.append(fun)
        
        elif command.startswith("google search "): # Handle Google search commands.
            fun = asyncio.to_thread (GoogleSearch, command.removeprefix("google search ")) # Schedule Google search.
            funcs.append(fun)

        elif command.startswith("youtube search "): # Handle YouTube search commands
            fun = asyncio.to_thread (YouTubeSearch, command.removeprefix("youtube search ")) # Schedule YouTube search.
            funcs.append(fun)
        
        elif command.startswith("system"): #Handle system commands.
            fun = asyncio.to_thread (System, command.removeprefix("system")) #Schedule system command.
            funcs.append(fun)
        else:
            print("No Function Found. For (command}") #Print an error for unrecognized commands.
        
    results = await asyncio.gather(*funcs) # Execute all tasks concurrently.

    for result in results: # Process the results.
        if isinstance(result, str): 
            yield result
        else:
            yield result

#Asynchronous function to automate command execution.
async def Automation (commands: list[str]):
    async for result in TranslateAndExecute(commands): # Translate and execute commands.
        pass
    return True # Indicate success.     

if __name__ == "__main__":
    asyncio.run(Automation([]))
  