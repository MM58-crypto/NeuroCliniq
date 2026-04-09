from fastapi import FastAPI, Request
import webhook_handler
from pyngrok import *
from pyngrok import ngrok
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN"))
public_url = ngrok.connect(8000)

app.include_router(webhook_handler.router)

@app.get("/")
async def root():
    return {"message": "Hello world"}



