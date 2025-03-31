import asyncio
import logging
import os
import requests
from dotenv import get_key
from PIL import Image
from random import randint
from time import sleep

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load API Key safely
API_KEY = get_key('.env', 'HuggingFaceAPIKey') or os.getenv("HuggingFaceAPIKey")
if not API_KEY:
    raise ValueError("🚨 Missing Hugging Face API Key!")

# API details
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Ensure Data directory exists
os.makedirs("Data", exist_ok=True)

def open_images(prompt):
    folder_path = "Data"
    prompt = prompt.replace(" ", "_")
    
    for i in range(1, 5):
        image_path = os.path.join(folder_path, f"{prompt}{i}.jpg")
        
        try:
            img = Image.open(image_path)
            logging.info(f"✅ Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            logging.warning(f"❌ Unable to open {image_path}")

async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            logging.error(f"🚨 API Error: {response.status_code} - {response.text}")
            return None
        
        return response.content
    except Exception as e:
        logging.error(f"❌ Request failed: {e}")
        return None

async def generate_images(prompt):
    tasks = []
    for _ in range(4):
        payload = {"inputs": f"{prompt}, quality=4K, high resolution, seed={randint(0, 1000000)}"}
        tasks.append(query(payload))
    
    image_bytes_list = await asyncio.gather(*tasks)
    
    for i, image_bytes in enumerate(image_bytes_list):
        if not image_bytes or not image_bytes.startswith(b'\xff\xd8'):
            logging.warning(f"❌ Invalid image data received for {prompt.replace(' ', '_')}{i + 1}.jpg")
            continue
        
        save_path = os.path.join("Data", f"{prompt.replace(' ', '_')}{i + 1}.jpg")
        with open(save_path, "wb") as f:
            f.write(image_bytes)
        logging.info(f"✅ Image saved: {save_path}")

def generate_images_sync(prompt):
    if asyncio.get_event_loop().is_running():
        asyncio.ensure_future(generate_images(prompt))
    else:
        asyncio.run(generate_images(prompt))
    open_images(prompt)

while True:
    try:
        with open("Frontend/Files/ImageGeneration.data", "r+") as f:
            data = f.read().strip()
            
            if not data:
                sleep(1)
                continue
            
            prompt, status = data.split(",")
            
            if status.strip().lower() == "true":
                logging.info("🎨 Generating Images...")
                generate_images_sync(prompt.strip())
                
                f.seek(0)
                f.write("False,False")
                f.truncate()
                break
            
            sleep(1)
    except :
        pass