import os
import threading
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok
from dotenv import load_dotenv

from app.routers import navigation

load_dotenv()

app = FastAPI(title="Indoor Navigation Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(navigation.router)

def start_ngrok():
    token = os.getenv("NGROK_AUTH_TOKEN")
    if token:
        ngrok.set_auth_token(token)
        public_url = ngrok.connect(8000, bind_tls=True).public_url
        print(f"\n✅ PUBLIC URL: {public_url}\n")
    else:
        print("⚠️ No Ngrok Token found. Run the server locally at http://0.0.0.0:8000")

if __name__ == "__main__":
    threading.Thread(target=start_ngrok, daemon=True).start()

    uvicorn.run(app, host="0.0.0.0", port=8000)
