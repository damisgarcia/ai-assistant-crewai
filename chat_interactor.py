"""
Chat Interactor - Simula conversas com o assistente virtual da clínica Dr. Garcia
"""
import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório src ao path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

load_dotenv()


class ChatInteractor:
    def __init__(self):
        """Inicializa o interator de chat"""
        self.conversation_history = []

    def start_conversation(self):
        """Inicia uma conversa interativa com o assistente"""
        print("🦷 Bem-vindo ao Assistente Virtual da Clínica Dr. Garcia!")
        print("Digite 'sair' ou 'quit' para encerrar a conversa.\n")

        from src.main import GarciaClinicAssistant
        assistant = GarciaClinicAssistant()

        if not assistant.initialize_system():
            print("❌ Falha ao inicializar o sistema. Verifique os logs para mais detalhes.")
            return

        while True:
          try:
            user_input = input("Você: ").strip()

            if user_input.lower() in ['sair', 'quit', 'exit']:
                print("Obrigado por usar nossos serviços! Até logo! 👋")
                break

            if not user_input:
                continue

            # Adiciona a mensagem do usuário ao histórico
            self.conversation_history.append({"role": "user", "content": user_input})

            # Processa a resposta usando o sistema principal
            try:
                response = assistant.process_user_query(user_input)
            except ImportError:
                # Fallback caso o sistema principal ainda não esteja implementado
                response = self.process_message_fallback(user_input)

            # Adiciona a resposta ao histórico
            self.conversation_history.append({"role": "assistant", "content": response})

            print(f"🦷 Assistente: {response}\n")

          except KeyboardInterrupt:
              print("\n\nConversa encerrada pelo usuário. Até logo! 👋")
              break
          except Exception as e:
              print(f"Erro durante a conversa: {e}")

    def process_message_fallback(self, message: str) -> str:
        """
        Resposta fallback quando o sistema principal não está disponível
        """
        return "Olá! Sou o assistente virtual da Clínica Dr. Garcia. No momento estou em desenvolvimento, mas em breve poderei ajudá-lo com informações sobre nossos serviços odontológicos!"

    def get_conversation_history(self):
        """Retorna o histórico da conversa"""
        return self.conversation_history

    def clear_history(self):
        """Limpa o histórico da conversa"""
        self.conversation_history = []


if __name__ == "__main__":
    chat = ChatInteractor()
    chat.start_conversation()
