from crewai import LLM,  Agent
from typing import List

class IntentAgent(Agent):
    def __init__(self, name="IntentAgent", role="Classificador de Intenções", llm=LLM, tools=List):
        goal = """
            Baseado na pergunta do usuário, classifique a intenção da conversa.
            Retorne APENAS UMA das seguintes opções sem explicação adicional:
            greeting: se o usuário está iniciando uma conversa ou apenas cumprimentando
            appointment: se o usuário está tentando agendar, fornecer dados para agendamento ou falar sobre uma consulta
            info: se o usuário deseja informações gerais sobre o consultório, serviços, procedimentos, horários, redes sociais e contatos
            unknown: se não for possível identificar a intenção com clareza
        """
        backstory = "Você é um agente que classifica a intenção com base na pergunta do usuário."
        super().__init__(name=name, role=role, goal=goal, backstory=backstory, tools=tools, llm=llm)
        self.verbose = True
