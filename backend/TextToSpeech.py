import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Initialize Pygame video subsystem at the start
pygame.init()

env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-GB-SoniaNeural")  # Default voice

async def TextToAudioFile(Text) -> None:
    file_path = r"Data\speech.mp3"
    if not os.path.exists("Data"):
        os.makedirs("Data")
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    communicate = edge_tts.Communicate(Text, str(AssistantVoice), pitch='+10Hz', rate='+15%')
    await communicate.save(file_path)

def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            asyncio.run(TextToAudioFile(Text))
            
            # Proper mixer initialization sequence
            if pygame.mixer.get_init() is None:
                pygame.mixer.pre_init(44100, -16, 2, 512)
                pygame.mixer.init()
            
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.event.pump()
                if not func():
                    break
                pygame.time.Clock().tick(10)
            
            return True
        
        except Exception as e:
            print(f"Error in TTS: {e}")
            pygame.time.wait(500)
        
        finally:
            try:
                func(False)
                if pygame.mixer.get_init() is not None:
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                break
            except Exception as e:
                print(f"Error in finally block: {e}")

def TextToSpeech(Text, func=lambda r=None: True):
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
    
    sentences = Text.split(".")
    if len(sentences) > 4 and len(Text) >= 250:
        selected = ". ".join(sentences[0:2]) + ". " + random.choice(responses)
        TTS(selected, func)
    else:
        TTS(Text, func)

if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the text: "))