import json

from channels.generic.websocket import WebsocketConsumer

from orchestrator import Orchestrator

from conversation.models import Conversation, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        payload = json.loads(text_data)

        type = payload.get("type")
        conversation_id = payload.get("conversation_id")
        content = payload["content"]

        orchestrator = Orchestrator()

        if type == "message":
            conversation = Conversation.objects.get(id=conversation_id)

            try:
                message = Message.objects.create(
                    conversation=conversation,
                    content=content,
                    sender_type="user",
                )

                self.send(text_data=json.dumps({
                    "type": "message",
                    "message": self.build_message(message)
                }))

                self.send(text_data=json.dumps({
                    "type": "typing",
                    "conversation_id": conversation_id,
                }))

                text_response = orchestrator.process_query(content)

                ai_message = Message.objects.create(
                    conversation=conversation,
                    content=text_response,
                    sender_type="ai_agent",
                )

                self.send(text_data=json.dumps({
                    "type": "message",
                    "message": self.build_message(ai_message)
                }))


            except Conversation.DoesNotExist:
                self.send(text_data=json.dumps({"error": "Conversation not found"}))
                return

    def build_message(self, message):
        return {
            "id": message.id,
            "conversation": message.conversation.id,
            "content": message.content,
            "sender_type": message.sender_type,
            "created_at": message.created_at.isoformat(),
            "updated_at": message.updated_at.isoformat(),
        }
