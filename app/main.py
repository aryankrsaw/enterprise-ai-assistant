from fastapi import FastAPI
from ollama import Client
from app.constants import SYSTEM_PROMPT
from app.model import ChatRequest, ChatResponse
from app.config import OLLAMA_API_KEY, OLLAMA_HOST, OLLAMA_MODEL


app = FastAPI()

client = Client(
    host=OLLAMA_HOST,
    headers={
        "Authorization": f"Bearer {OLLAMA_API_KEY}"
    }
)
print("Connection completed to Ollama...")

conversation_memory = {}
MAX_HISTORY_MESSAGES = 10

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    history = []

    history = conversation_memory.get(request.conversation_id,[])

  # Storing the new user message
    history.append({
        "role": "user",
        "content": request.message
    })

    # Keeping only recent conversation
    recent_history = history[-MAX_HISTORY_MESSAGES:]

    # Included system prompt
    messages=[
        SYSTEM_PROMPT,
        *recent_history
    ]

    # Calling LLM
    model_response = client.chat(
        model=OLLAMA_MODEL,
        messages=messages
    )

    assistant_message = model_response["message"]["content"]

    history.append({
        'role':'assistant',
        'content':assistant_message
    })

    conversation_memory[request.conversation_id]=history

    return ChatResponse(
        response=assistant_message
    )