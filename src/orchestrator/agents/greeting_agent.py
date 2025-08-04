from crewai import LLM,  Agent

class GreetingAgent(Agent):
  def __init__(self, name="GreetingAgent", role="Agente de Boas-Vindas", llm=LLM, tools=None):
      goal = "Responder com uma mensagem de boas-vindas passe informações básicas da clínica."
      backstory = "Você é um atendente cordial e prestativo."
      super().__init__(name=name, role=role, goal=goal, backstory=backstory, llm=llm)
      self.verbose = True  # Desativa o modo verbose para evitar logs excessivos
      self.tools = tools if tools is not None else []
