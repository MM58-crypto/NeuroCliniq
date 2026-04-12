from fastapi import FastAPI, Request, APIRouter, Response, HTTPException
import logging
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")

router = APIRouter(prefix="/webhook", tags=["webhook"])


#@app.webhooks.post("")
#async def receive_message(request: Request):
#    data = await request.json()
#    print(data)  # your WhatsApp message lands here
#    return {"status": "ok"}

@router.get("")
async def verify_webhook(request: Request):
    params = request.query_params

    mode      = params.get("hub.mode")
    token     = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("Webhook verified successfully ")
        return Response(content=challenge, media_type="text/plain")

    logger.warning("Webhook verification failed ")
    raise HTTPException(status_code=403, detail="Verification failed")

@router.post("")
async def receive_message(request: Request):
    data = await request.json()
    logger.info(f"Incoming payload: {data}")

    try:
        entry = data.get("entry", [])

        if not entry:
            return {"status": "no entry"}

        changes = entry[0].get("changes", [])

        if not changes:
            return {"status": "no changes"}

        value = changes[0].get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "no messages"}

        message = messages[0]

        sender  = message.get("from")
        msg_type = message.get("type")

        if msg_type == "text":
            text = message["text"]["body"]
            logger.info(f"Message from {sender}: {text}")

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return {"status": "error"}
