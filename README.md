# OpenAI.FM Audio Generation Automation

This Colab notebook provides a solution to automate the process of converting large text inputs into audio using the OpenAI.FM web service. Due to limitations on the input text length on the website, the notebook implements a text chunking strategy to split the input into smaller, manageable parts, generate audio for each part, and then merge the resulting audio segments into a single output file.

## Problem

The OpenAI.FM website has a character limit for the text input when generating audio. For longer texts, this limit prevents generating audio in a single operation.

## Solution

This notebook automates the following steps:

1. **Splitting the text**: The input text is split into smaller chunks that comply with the website's character limit.  
2. **Generating audio**: For each text chunk, the notebook interacts with the OpenAI.FM website using Selenium to input the text, select a voice, and trigger the audio generation and download process.  
3. **Merging audio**: The downloaded audio files (one for each chunk) are merged into a single, continuous audio file.  

## Setup

1. **Install Dependencies**

   ```bash
   !pip install selenium pydub chromium-chromedriver
   ```

2. **Setup the Environment**

   ```python
   import os
   from selenium import webdriver
   from selenium.webdriver.chrome.service import Service
   from selenium.webdriver.chrome.options import Options
   import time

   download_dir = '/content'
   os.makedirs(download_dir, exist_ok=True)

   # Setup Chrome options for Selenium
   chrome_options = Options()
   chrome_options.add_argument('--headless')
   chrome_options.add_argument('--no-sandbox')
   chrome_options.add_argument('--disable-dev-shm-usage')

   driver = webdriver.Chrome(service=Service(), options=chrome_options)
   website_url = "https://www.openai.fm"
   driver.get(website_url)
   time.sleep(3)
   ```

## Text Splitting Strategy

To handle long text inputs, the notebook splits the text into smaller parts. Each part adheres to the character limit and tries to end at a logical break (e.g., at the last complete sentence or word boundary).

```python
def split_text_into_parts(text, max_length=900):
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
                # Extend to next dot if possible
                next_dot = text.find('.', end)
                split_point = next_dot + 1 if next_dot != -1 else text_length

        if split_point == start:  # avoid infinite loop
            split_point = min(start + max_length, text_length)

        parts.append(text[start:split_point].strip())
        start = split_point

    return parts
```

## Audio Generation and Merging

After splitting the text into manageable chunks, the notebook automates audio generation using Selenium and merges the resulting audio files into one final file.

```python
from pydub import AudioSegment
import glob
import os

folder_path = "/content"
output_path = "merged_output.wav"

# Collect all audio files in the download folder
audio_files = sorted(glob.glob(os.path.join(folder_path, "*.mp3")))
audio_files.insert(0, audio_files.pop())  # Adjust the order if necessary

combined = AudioSegment.empty()

for audio_file in audio_files:
    try:
        audio = AudioSegment.from_wav(audio_file)  # Try WAV first
        combined += audio
    except:
        try:
            audio = AudioSegment.from_mp3(audio_file)  # Fallback to MP3
            combined += audio
        except Exception as e:
            print(f"Could not process {audio_file}: {e}")
            continue

combined.export(output_path, format="wav")
print("Contents of /content:")
for item in os.listdir('/content'):
    print(item)
```

## Usage

- **Upload Your Text**: Provide the input text in the notebook (ensure it's within a reasonable length or let it be chunked).  
- **Run the Notebook**: Execute the cells to automatically split the text, generate audio, and merge the files.  
- **Download the Output**: Once the audio is merged, the resulting file will be available for download as `merged_output.wav`.  

## Notes

- The notebook is optimized for use in Google Colab, but can be adapted for local setups with proper installation of Selenium and other dependencies.  
- The `pydub` library supports both MP3 and WAV formats. The merged audio will be saved as a WAV file.  
- If the website experiences downtime or changes in its interface, the notebook may require updates.  

