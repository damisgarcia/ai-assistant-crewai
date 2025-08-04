from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

from conversation.models import Conversation, Message
from conversation.models import CONVERSATION_STATUS_OPEN, CONVERSATION_STATUS_REGISTERING_CONTACT
from typing import List

class ConversationIdInput(BaseModel):
    """Input schema for RagTool."""
    conversation_id: int = Field(..., description="Id da conversa")

class FetchUserMessageTool(BaseTool):
  name: str = "fetch_user_messages"
  description: str = "Busca as últimas mensagens do usuário na conversa"
  args_schema: Type[BaseModel] = ConversationIdInput

  def __init__(self):
        super().__init__()

  def _run(self, conversation_id: int) -> List[str]:
    """Fetch the latest user messages from the conversation."""
    try:
      # Fetch the latest user messages from the database
      latest_messages = Message.objects.filter(
        conversation_id=conversation_id, sender_type="user"
      ).order_by("-created_at")[:15]

      return [message.content for message in latest_messages]

    except Exception as e:
      return []

class ChangeStatusRegisteringContactTool(BaseTool):
  name: str = "change_status_registering_contact"
  description: str = "Altera o status da conversa para 'registering_contact'"
  args_schema: Type[BaseModel] = ConversationIdInput

  def __init__(self):
    super().__init__()

  def _run(self, conversation_id: int) -> bool:
    """Change the status of the conversation."""
    try:
      conversation = Conversation.objects.get(id=conversation_id, status=CONVERSATION_STATUS_OPEN)
      conversation.status = CONVERSATION_STATUS_REGISTERING_CONTACT
      conversation.save()
      return True
    except Exception as e:
      return False
