from fastapi import FastAPI
from ollama import Client
from app.constants import SYSTEM_PROMPT
from app.model import ChatRequest, ChatResponse
from app.config import OLLAMA_API_KEY, OLLAMA_HOST, OLLAMA_MODEL
from app.rag.retrieval import search_similar_chunks


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

    # Retrieve relevant chunks from the PDF
    relevant_chunks = search_similar_chunks(
        request.message,
        top_k=3
    )

    # Convert retrieved chunks into a single context
    context = "\n\n".join(relevant_chunks)

    history = conversation_memory.get(
        request.conversation_id,
        []
    )

    # Store the new user message
    history.append({
        "role": "user",
        "content": request.message
    })

    # Keep only recent conversation
    recent_history = history[-MAX_HISTORY_MESSAGES:]

    # Create RAG prompt
    rag_prompt = f"""
        Use the following context to answer the user's question.

        Context:
        {context}

        Question:
        {request.message}

        Instructions:
        - Answer using only the provided context.
        - Do not make up information.
        - If the answer is not present in the context, say that you don't know.
    """

    # Messages sent to the LLM
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        *recent_history[:-1],
        {
            "role": "user",
            "content": rag_prompt
        }
    ]

    # Calling LLM
    model_response = client.chat(
        model=OLLAMA_MODEL,
        messages=messages
    )

    assistant_message = model_response["message"]["content"]

    # Store assistant response
    history.append({
        "role": "assistant",
        "content": assistant_message
    })

    conversation_memory[request.conversation_id] = history

    return ChatResponse(
        response=assistant_message
    )