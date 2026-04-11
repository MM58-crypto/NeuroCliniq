from google import genai
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_key)

db_pass = os.getenv("DB_PASSWORD")

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=db_pass,
        host="localhost",
        port=5432
    )
    cursor = conn.cursor()
except Exception as e:
    print(f"An error occurred while connecting to DB: {e}")


def fetch_faqs():
    cursor.execute("SELECT question, answer FROM faqs;")
    rows = cursor.fetchall()
    # formats each row into readable text before injecting into prompt
    return "\n".join([f"Q: {row[0]}\nA: {row[1]}" for row in rows])


def ask(user_question):
    faq_context = fetch_faqs()

    prompt = f"""
You are a helpful clinic assistant.
You must answer ONLY based on the information provided below.
If the answer is not found in the provided information, respond with:
"عذراً، لا تتوفر لديّ معلومات كافية للإجابة على هذا السؤال."
Do not generate, assume, or infer any information beyond what is provided.

--- AVAILABLE INFORMATION ---
{faq_context}
--- END OF INFORMATION ---

Patient question: {user_question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"


# test loop
while True:
    user_input = input("Ask a question (or type 'exit'): ")
    if user_input.lower() == "exit":
        break
    print(f"\nBot: {ask(user_input)}\n")
