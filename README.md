**Automated Text-to-Speech Generator**
---
This project automates the process of converting long text into a single audio file using a web-based text-to-speech interface.

It is designed to handle real-world limitations like character limits, repetitive UI interaction, and fragmented audio output, and turn them into a smooth, end-to-end pipeline.

---

**What This Does**
---
> Takes long-form text as input
> 
> Splits it into manageable chunks

> Automatically generates audio for each chunk using browser automation
> 
> Downloads all audio files
> 
> Merges them into one continuous output file
> 
> No manual clicking. No copy-paste loops.

---
**Why This Exists**
---
Most online TTS tools:

Limit how much text you can process at once

Require repetitive manual interaction

Export audio in fragments

This project treats those as engineering constraints and builds around them instead of fighting the tool.

---
**How It Works**
---
**Text splitting**
Long input is split into chunks under a safe character limit, with preference for sentence boundaries.

**Browser automation**
Selenium runs a headless browser, opens multiple tabs, injects text, triggers audio generation, and downloads the results.

**Audio merging**
All downloaded files are decoded and merged into a single WAV file.

The logic is intentionally defensive to handle UI delays, alerts, and inconsistent audio formats.

---
**Tech Stack**
---
Python

Selenium (Chromium, headless)

PyDub

Regular expressions

Basic OS-level file handling

----
**Setup**
----
Install Python dependencies:

pip install selenium pydub

---
**System dependencies (Linux / Colab):**
---
apt-get update
apt install chromium-chromedriver


Make sure ffmpeg is available for audio processing.

---
**Usage**
---
Run the script and enter the text when prompted.
After completion, you’ll get:

merged_output.wav


This file contains the full narration of the original input text.

---
**Notes**
---
Handles long text automatically

Works headless (no visible browser)

Designed to fail gracefully if the UI behaves unexpectedly

---
**Author**
---
Sana Ilahi

BSIT student, focused on Python automation and practical problem-solving

---
