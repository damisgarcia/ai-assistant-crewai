from crewai import LLM,  Agent

class GreetingAgent(Agent):
  def __init__(self, name="GreetingAgent", role="Agente de Boas-Vindas", llm=LLM):
      goal = "Responder com uma mensagem de boas-vindas passe informações básicas da clínica."
      backstory = "Você é um atendente cordial e prestativo."
      super().__init__(name=name, role=role, goal=goal, backstory=backstory, llm=llm)
      self.verbose = True