from fastapi import FastAPI
from ollama import Client

from app.model import ChatRequest, ChatResponse
from app.config import OLLAMA_API_KEY, OLLAMA_HOST, OLLAMA_MODEL

app = FastAPI()

client = Client(
    host=OLLAMA_HOST,
    headers={
        "Authorization": f"Bearer {OLLAMA_API_KEY}"
    }
)


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    model_response = client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": """
                You are an Enterprise AI Assistant.

                Your responsibilities:
                1. Give accurate and useful answers.
                2. Explain technical concepts clearly.
                3. Do not invent information when you are uncertain.
                4. Prefer concise answers unless detailed explanation is requested.
                5. When explaining technical topics, provide examples where useful.
                6. Answer within 100 words.
                """
            },
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    return ChatResponse(
        response=model_response["message"]["content"]
    )