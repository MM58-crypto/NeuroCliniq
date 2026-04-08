from fastapi import FastAPI, Request
import webhook_handler

app = FastAPI()



app.include_router(webhook_handler)

@app.get("/")
async def root():
    return {"message": "Hello world"}



