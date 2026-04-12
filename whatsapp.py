import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

WHATSAPP_API_URL = "https://graph.facebook.com/v21.0"
PHONE_NUMBER_ID  = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
ACCESS_TOKEN     = os.getenv("WHATSAPP_BEARER_TOKEN")


async def send_text_message(to: str, message: str):
    url = f"{WHATSAPP_API_URL}/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Message sent to {to}: {response.status_code}")
            return response.json()

    except httpx.HTTPStatusError as e:
        logger.error(f"WhatsApp API error: {e.response.status_code} - {e.response.text}")
        raise

    except Exception as e:
        logger.error(f"Failed to send message to {to}: {e}")
        raise
