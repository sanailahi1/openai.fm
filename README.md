# OpenAI.fm Audio Merger

A Python script that automates converting text into speech using [OpenAI.fm](https://www.openai.fm), downloads the generated audio segments via Selenium, merges them into a single audio file with `pydub`, plays it back using `pygame`, and finally cleans up temporary files.

---

## Features

* **Text splitting**: Breaks long texts into chunks (max 900 characters) to comply with site limits.
* **Browser automation**: Uses Selenium to open multiple tabs, submit text segments, and download audio files.
* **Download management**: Waits for Chrome downloads to finish and tracks downloaded files.
* **Audio merging**: Concatenates all downloaded `.wav` segments into one `merged_audio.wav`.
* **Playback**: Plays the merged audio automatically.
* **Cleanup**: Deletes all downloaded and temporary files after playback.

---

## Prerequisites

* **Python 3.7+**
* **Google Chrome** (and matching ChromeDriver)
* **Packages**:

  * [selenium](https://pypi.org/project/selenium/)
  * [pydub](https://pypi.org/project/pydub/)
  * [pygame](https://pypi.org/project/pygame/)

Install Python packages via pip:

```bash
pip install selenium pydub pygame
```

---

## Installation

1. Clone this repository or download `openaifm.py`.
2. Ensure you have Chrome installed and download the appropriate [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/).
3. Place `chromedriver.exe` somewhere on your system (e.g., `C:\chromedriver\chromedriver.exe`).

---

## Configuration

Edit the following variables at the top of `openaifm.py`:

```python
chrome_driver_path = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'  # Path to ChromeDriver
chrome_path        = 'C:\Program Files\Google\Chrome\Application\chrome.exe'       # Path to Chrome binary
```

Optionally, adjust:

* `download_dir`: Directory where audio files will be saved (defaults to `~/New folder`).
* Chrome options (headless mode, sandbox flags).

---

## Usage

Run the script and enter the text you want to convert when prompted:

```bash
python openaifm.py
```

1. The script will split your input into chunks of up to 900 characters.
2. For each chunk, it opens a new browser tab, submits the text to OpenAI.fm, and downloads the resulting audio file.
3. After all segments are downloaded, they are merged into `merged_audio.wav`.
4. The merged audio plays automatically via `pygame`.
5. Temporary files are deleted.

---

## How It Works

1. **Splitting Text**: The `split_text_into_parts` function ensures each segment is under 900 characters, splitting at sentence boundaries or word breaks.
2. **Selenium Automation**:

   * Opens the OpenAI.fm website in multiple tabs.
   * Fills in the conversion settings (voice/personality) and text.
   * Clicks generate and download buttons.
   * Waits for downloads to complete using `wait_for_download`.
3. **File Handling**:

   * `get_latest_file` identifies the most recently downloaded file in the directory.
   * Downloaded `.wav` files are tracked in `downloaded_files`.
4. **Audio Merging**: The script uses `pydub.AudioSegment` to concatenate all `.wav` files into one.
5. **Playback**: Uses `pygame.mixer` to play the merged audio.
6. **Cleanup**: Removes all files from the download directory after playback.

---

## Troubleshooting

* **No audio downloaded?**

  * Ensure XPaths in the script match the current OpenAI.fm page structure.
  * Check that `chrome_options` allow automatic downloads.

* **ChromeDriver errors?**

  * Verify `chrome_driver_path` and `chrome_path` are correct.
  * Ensure ChromeDriver version matches your Chrome browser version.

* **Merge issues?**

  * Confirm downloaded files have `.wav` extension.
  * Check for incomplete `.tmp` files in the download directory.

---

## License

This project is licensed under the MIT License. Feel free to use and modify it for your needs.
