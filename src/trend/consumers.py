import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

from orchestrator import Orchestrator

from conversation.models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        # Log da desconexão ou qualquer limpeza necessária
        print(f"WebSocket disconnected with code: {close_code}")
        raise StopConsumer()

    async def receive(self, text_data):
        try:
            payload = json.loads(text_data)

            type = payload.get("type")
            conversation_id = payload.get("conversation_id")
            content = payload["content"]

            orchestrator = Orchestrator()

            if type == "message":
                try:
                    conversation = await Conversation.objects.aget(id=conversation_id)
                except Conversation.DoesNotExist:
                    await self.send(text_data=json.dumps({"error": "Conversation not found"}))
                    return

                message = await Message.objects.acreate(
                    conversation=conversation,
                    content=content,
                    sender_type="user",
                )

                try:
                    await self.send(text_data=json.dumps({
                        "type": "message",
                        "message": self.build_message(message)
                    }))
                except Exception as e:
                    print(f"Erro ao enviar mensagem do usuário: {e}")
                    return # Conexão provavelmente fechada

                try:
                    await self.send(text_data=json.dumps({
                        "type": "typing",
                        "conversation_id": conversation_id,
                    }))
                except Exception as e:
                    print(f"Erro ao enviar status de digitação: {e}")
                    return # Conexão provavelmente fechada

                # Se orchestrator.process_query é síncrono, continue a rodá-lo em um thread
                loop = asyncio.get_event_loop()
                text_response = await loop.run_in_executor(
                    None, orchestrator.process_query, content, conversation_id
                )

                ai_message = await Message.objects.acreate(
                    conversation=conversation,
                    content=text_response,
                    sender_type="ai_agent",
                )

                try:
                    await self.send(text_data=json.dumps({
                        "type": "message",
                        "message": self.build_message(ai_message)
                    }))
                except Exception as e:
                    print(f"Erro ao enviar mensagem do AI: {e}")
                    return # Conexão provavelmente fechada
        except Exception as e:
            print(f"Erro geral no receive: {e}")
            # Opcional: enviar uma mensagem de erro para o cliente antes de fechar
            # await self.close()

    def build_message(self, message):
        return {
            "id": message.id,
            "conversation": message.conversation.id,
            "content": message.content,
            "sender_type": message.sender_type,
            "created_at": message.created_at.isoformat(),
            "updated_at": message.updated_at.isoformat(),
        }
