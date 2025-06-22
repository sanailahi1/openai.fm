from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import os
from selenium.webdriver.chrome.options import Options
from pydub import AudioSegment
import pygame
import re
import glob, time

def wait_for_download(directory, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        files = glob.glob(os.path.join(directory, "*"))
        if files:
            # you can even check for “.crdownload” temporary files disappearing
            if all(not f.endswith(".crdownload") for f in files):
                return files
        time.sleep(1)
    raise TimeoutError(f"No files showed up in {directory} after {timeout}s")


# ChromeDriver ka path (apne system ke hisaab se set karo)
chrome_driver_path = 'c:\Program Files\Google\Chrome\Application\chromedriver.exe'  # Set your chromedriver path
chrome_path = 'c:\Program Files\Google\Chrome\Application\chrome.exe'  # Set your Chrome path
# 1. Ensure folder exists
download_dir = os.path.expanduser("~") + '\\New folder'
os.makedirs(download_dir, exist_ok=True)

# 2. Chrome options
#run in headless mode (optional)
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_path  # Set the path to Chrome binary
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "profile.default_content_settings.popups": 0,
    "safebrowsing.enabled": True,
    "safebrowsing.disable_download_protection": True
})

driver = webdriver.Chrome(service=Service(chrome_driver_path),
                          options=chrome_options)
# Website URL
website_url = "https://www.openai.fm"  # Replace with actual URL

# Open main website tab once.
driver.get(website_url)
time.sleep(3)  # Wait for page load

# Function to split text into parts of up to 900 chars, splitting at line breaks for flow
def split_text_into_parts(text, max_length=900):
  
    """
    Splits the input text into parts, each not exceeding the character limit.
    Each part ends at the last complete sentence (ending with a dot).
    If no dot is found, splits at the last word boundary (space).
    If neither is found, includes the unsplit segment at the start of the next part.
    """
    parts = []
    start = 0
    text_length = len(text)
    
    
    while start < text_length:
        end = min(start + max_length, text_length)
        part = text[start:end]
        
        # Try to split at the last dot
        last_dot = part.rfind('.')
        if last_dot != -1:
            split_point = start + last_dot + 1
        else:
            # Try to split at the last space
            last_space = part.rfind(' ')
            if last_space != -1 and end < text_length:
                split_point = start + last_space
            else:
                # No suitable split point found, extend to next dot after limit
                next_dot = text.find('.', end)
                if next_dot != -1:
                    split_point = next_dot + 1
                else:
                    # No dot found, take the rest of the text
                    split_point = text_length
        
        # If split_point didn't advance, avoid infinite loop by moving at least one character
        if split_point == start:
            split_point = min(start + max_length, text_length)
        
        # Append the part and update the start index
        parts.append(text[start:split_point].strip())
        start = split_point
    
    return  parts





# Function to remove non-BMP characters from a string
def remove_non_bmp_characters(text):
    return re.sub(r'[^\u0000-\uFFFF]', '', text)

# Text to convert
text_to_convert = input("Enter the text to convert: ")



# Split the text into parts
text_parts = split_text_into_parts(text_to_convert)

# Function to get the latest file in the directory
def get_latest_file(directory):
    files = os.listdir(directory)
    paths = [os.path.join(directory, file) for file in files if os.path.isfile(os.path.join(directory, file))]
    
    # Log the files and paths for debugging
    if not paths:
        print(f"No files found in directory: {directory}")
        raise FileNotFoundError(f"No files found in the directory: {directory}")
    
    # Log file paths and their modification times for debugging
    for path in paths:
        print(f"File: {path}, Modification Time: {os.path.getmtime(path)}")
    
    # Use modification time to find the latest file
    return max(paths, key=os.path.getmtime)

# List to store downloaded file paths
downloaded_files = []

# Create multiple tabs based on the number of text parts
for _ in range(len(text_parts) - 1):  # Create additional tabs (one less since the first tab is already open)
    driver.execute_script("window.open('');")

# Perform initial setup (clicks and placeholder removal) on each tab
for i, part in enumerate(text_parts):
    driver.switch_to.window(driver.window_handles[i])  # Switch to the respective tab

    # Open the website in the current tab
    driver.get(website_url)
    time.sleep(3)  # Wait for the page to load

    # Perform initial setup: click voice and clear the placeholder
    character_name = driver.find_element(By.XPATH, "/html/body/div/main/div[1]/div/div[2]/div/div[6]/div")
    character_name.click()
    instructions_field = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[2]/div/textarea")
    # Clear the placeholder text
    instructions_field.clear()
    # Fill in the instructions field with a placeholder text
    instructions_field.send_keys('''Affect/personality: A cheerful guide 

Tone: Friendly, clear, and reassuring, creating a calm atmosphere and making the listener feel confident and comfortable.

Pronunciation: Clear, articulate, and steady, ensuring each instruction is easily understood while maintaining a natural, conversational flow.

Pause: Brief, purposeful pauses after key instructions (e.g., "cross the street" and "turn right") to allow time for the listener to process the information and follow along.

Emotion: Warm and supportive, conveying empathy and care, ensuring the listener feels guided and safe throughout the journey.''')  # Adjust as needed
    time.sleep(0.5)  # Wait for the field to be filled

    text_input = driver.find_element(By.ID, "prompt")
    text_input.clear()

    # Remove non-BMP characters from the text part
    sanitized_part = remove_non_bmp_characters(part)

    # Fill in the text input with the sanitized part text
    text_input.send_keys(sanitized_part)

    # Wait until the generate button is clickable and then click it
    generate_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/footer/div/div/div[3]/div"))
    )
    
    # Click the generate button
    generate_button.click()

    time.sleep(3)  # Wait for the response

    # Locate and click the download button (adjust XPath as needed)
    download_button = driver.find_element(By.XPATH, "/html/body/div/footer/div/div/div[1]")
    download_button.click()

    downloaded = wait_for_download(download_dir, timeout=30)
    print("Got files:", downloaded)

     # Adjust the sleep time as needed for download completion
    latest_file = get_latest_file(download_dir)
    downloaded_files.append(latest_file)

# Close all tabs and quit the browser
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    driver.close()

# Quit the browser

driver.quit()

# Merge all downloaded audio files using pydub
merged_audio = AudioSegment.empty()
processed_files = set()  # Unique file names ya paths

for file in downloaded_files:
    if file.endswith(".tmp"):
        print(f"File is still downloading: {file}")
        print("Waiting for download to complete...")
        time.sleep(4) 
    if file.endswith(".wav"):
        filename = os.path.basename(file).lower().strip()  # lower-case + clean whitespace
        print(f"Merging file: {filename}")
        audio = AudioSegment.from_file(file)
        merged_audio += audio
        processed_files.add(filename)  # exact filename
    

    else:
        print(f"Downloaded file format galat hai: {file}")


# Save the merged audio file
merged_audio_file = os.path.join(download_dir, "merged_audio.wav")
merged_audio.export(merged_audio_file, format="wav")
print(f"Merged audio file saved at: {merged_audio_file}")

# Ensure the file path is properly formatted
merged_audio_file = os.path.normpath(merged_audio_file)

# Initialize pygame mixer and play the audio file
pygame.mixer.init()
pygame.mixer.music.load(merged_audio_file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)
# Delete all the files in the directory
for file in os.listdir(download_dir):
    file_path = os.path.join(download_dir, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)  # Remove the file
            print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
