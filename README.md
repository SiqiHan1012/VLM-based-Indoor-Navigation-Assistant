# 🤖 Real-Time Vision-Language Indoor Navigation System

## 🌟 Overview

This project implements a real-time, voice-controlled indoor navigation system using a combination of a fast-API server, a Vision-Language Model (VLM) for perception, and an Automatic Speech Recognition (ASR) system for command input.

The server is designed for quick deployment, particularly on platforms like Google Colab using Ngrok, allowing a mobile device to act as the camera/microphone input and the navigation guidance display. The system provides real-time "next action" instructions (e.g., "Step forward," "Keep left") and voice feedback to guide a user towards a specified goal.

## ✨ Features

  * **Real-Time VLM Inference:** Processes video frames streamed from a mobile device to generate navigation actions.
  * **Voice Control (ASR):** Users can set a navigation goal or issue commands (START/STOP) using their voice.
  * **Text-to-Speech (TTS) Guidance:** Provides spoken navigation instructions and feedback (e.g., announcing the new goal or next action).
  * **Mobile Web Client:** The front-end is a single HTML/JavaScript page optimized for mobile browsers to capture video/audio streams.
  * **API Compatibility:** Utilizes the **DashScope (Qwen-VL)** VLM via the OpenAI compatible API standard for seamless integration.
  * **Colab/Ngrok Deployment:** Easy setup for public access, enabling testing with personal mobile devices without complex networking.

## ⚙️ Prerequisites

Before running the server, you must have the following:

1.  **Python 3.9+**
2.  **Ngrok Account & Auth Token:** Required to expose the local Colab server to the public internet for mobile access.
3.  **VLM API Key (e.g., DashScope/Aliyun):** The system relies on the `DASHSCOPE_API_KEY` for vision-language inference.
4.  A **Mobile Device** (iOS/Android) for testing the camera and microphone input.

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd IndoorNav # Adjust this to your project's root directory name
```

### 2. Install Dependencies

The project relies on libraries like FastAPI, Uvicorn, pyngrok, PIL, and the OpenAI client library.

```bash
# Assuming you have a requirements.txt file
pip install -r requirements.txt
# Ensure you also install python-dotenv for environment variable management
pip install python-dotenv
```

### 3. Configuration (`.env` file)

Create a file named `.env` in your project's root directory and populate it with your API keys and tokens.

```
# .env file content
# Ngrok token is essential for public access (Colab)
NGROK_AUTH_TOKEN="<YOUR_NGROK_AUTH_TOKEN_HERE>"

# Vision-Language Model API Key (DashScope/Qwen-VL)
DASHSCOPE_API_KEY="<YOUR_DASHSCOPE_API_KEY_HERE>"

# (Optional) If you use a separate ASR service like OpenAI Whisper, add the key here
# OPENAI_API_KEY="<YOUR_OPENAI_API_KEY_HERE>" 
```

## 💻 Quick Start: Deploying on Google Colab

The easiest way to run this server and access it from your mobile phone is via a Google Colab notebook.

### Colab Cell 1: Environment Setup

Mount your Google Drive (if needed) and set the working directory to your project root (e.g., `IndoorNav`), then install dependencies and load environment variables.

```python
import os
from dotenv import load_dotenv

# --- Set your project root path ---
PROJECT_DIR = "/content/drive/MyDrive/2025Fall/ECE1724H/IndoorNav" 
os.chdir(PROJECT_DIR) 
print(f"Current working directory set to: {os.getcwd()}")

# --- Install Dependencies and Load .env ---
!pip install -r requirements.txt
!pip install python-dotenv

load_dotenv(".env")
print("\nEnvironment loaded. Checking NGROK_AUTH_TOKEN:", os.getenv("NGROK_AUTH_TOKEN") is not None)
```

### Colab Cell 2: Run the Server

Execute the main server file using Python's **module execution mode (`-m`)** to correctly handle imports.

```python
# Replace 'app.main' with the path to your main server file 
# (e.g., app.main if server is at app/main.py)
!python -m app.main 
```

Upon successful execution, the output will display the public Ngrok URL:

```
✅ PUBLIC URL: https://xxxx-xxx-xx-xxx-xx.ngrok-free.app
```

## 📱 Usage

1.  **Access the Client:** Open the **PUBLIC URL** in the browser of your mobile device (recommended: Safari on iOS, Chrome on Android).
2.  **Enable Voice:** Tap the **"🎙 Enable Voice"** button and grant microphone permission. This also prepares the system for navigation.
3.  **Start Video:** Tap the **"🎥 Start"** button and grant camera permission. The video stream will start sending frames to the VLM server.
4.  **Set Goal:**
      * **Voice:** Say a command like "Direct me to the office door."
      * **Manual:** You can implement a manual text input for the goal (if your HTML supports it).
5.  **Receive Guidance:** The system will provide visual (HUD) and auditory (TTS) instructions on the next steps (e.g., "Step forward," "Your destination is ahead on your left").

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `app/main.py` | The main FastAPI server entry point. Sets up Ngrok, defines API routes (`/infer`, `/asr`, `/`), and serves the front-end client. |
| `run_video_demo_correct.py` | Contains the core VLM logic, including pre-veto checks, scene hint building, and final action decision-making. |
| `api_client_openai_compat.py` | Handles communication with the DashScope/Qwen-VL API using the OpenAI compatibility layer. |
| `requirements.txt` | Lists all necessary Python dependencies. |
| `.env` | Configuration file for storing sensitive API keys and tokens. |

## 🙏 Acknowledgements

This project utilizes:

  * FastAPI for the web server.
  * Uvicorn as the ASGI server.
  * Ngrok for public tunneling.
  * DashScope/Qwen-VL for Vision-Language Model inference.

## 📄 License

[Place your license information here, e.g., MIT License]
