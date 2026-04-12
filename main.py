from fastapi import FastAPI, Request
import webhook_handler
import ngrok
import uvicorn
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv
from loguru import logger
import psycopg2


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
"""
db_pass = os.getenv("DB_PASSWORD")
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=db_pass,
        host="localhost",
        port=5432
    )
    cursor = conn.cursor() #?

    cursor.execute("SELECT * FROM patients;")
    print(cursor.fetchone())

except Exception as e:
    print(f"An error occurred (DB): {e}")
"""
@app.get("/")
async def root():
    return {"message": "Hello world"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
