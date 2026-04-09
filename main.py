from fastapi import FastAPI, Request
import webhook_handler
import ngrok
import uvicorn
#from pyngrok import *
#from pyngrok import ngrok
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()
app = FastAPI()

ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN"))
APPLICATION_PORT=8000
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Setting up ngrok endpoint")
    ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN"))
    tunnel = await ngrok.forward(
        addr=APPLICATION_PORT,
    )
    logger.info(f"Public URL: {tunnel.url()}")
    yield
    logger.info("Tearing down ngrok endpoint")
    ngrok.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(webhook_handler.router)

@app.get("/")
async def root():
    return {"message": "Hello world"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
