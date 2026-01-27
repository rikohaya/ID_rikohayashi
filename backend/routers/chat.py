from fastapi import APIRouter, HTTPException
from backend import database as db
from backend.services import gemini
from backend.models import (
    ChatRequest,
    ChatResponse,
    ConversationCreate,
    ConversationResponse,
    ConversationWithMessages,
    MessageResponse,
)

router = APIRouter(prefix="/api", tags=["chat"])


@router.get("/conversations", response_model=list[ConversationResponse])
async def get_conversations():
    conversations = await db.get_conversations()
    return conversations


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(data: ConversationCreate = ConversationCreate()):
    conversation = await db.create_conversation(data.title)
    return conversation


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(conversation_id: int):
    conversation = await db.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int):
    success = await db.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted successfully"}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    conversation_id = request.conversation_id

    if not conversation_id:
        conversation = await db.create_conversation()
        conversation_id = conversation["id"]

        title = await gemini.generate_title(request.message)
        await db.update_conversation_title(conversation_id, title)
    else:
        conversation = await db.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

    user_message = await db.add_message(conversation_id, "user", request.message)

    messages = await db.get_conversation_messages(conversation_id)
    messages = messages[:-1]

    ai_response = await gemini.generate_response(messages, request.message)

    assistant_message = await db.add_message(conversation_id, "assistant", ai_response)

    return ChatResponse(
        conversation_id=conversation_id,
        user_message=MessageResponse(**user_message),
        assistant_message=MessageResponse(**assistant_message),
    )
