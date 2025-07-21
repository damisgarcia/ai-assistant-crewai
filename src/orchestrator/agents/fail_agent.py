from crewai import LLM,  Agent

class FailAgent(Agent):
  def __init__(self, name="FailAgent", role="Assistente de Falhas", llm=LLM):
    goal = "Responder com uma mensagem de desconhecimento da pergunta, pergunte como posso ajudar?"
    backstory = "Você é um atendente cordial e prestativo, mas não entendeu a pergunta."
    super().__init__(name=name, role=role, goal=goal, backstory=backstory, llm=llm)
    self.verbose = True