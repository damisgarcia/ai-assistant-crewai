from crewai import LLM,  Agent

class InfoAgent(Agent):
  def __init__(self, name="InfoAgent", role="Assistente de Informações", llm=LLM, tools=None):
      goal = "Fornecer informações estritamente sobre a clínica, como localização, horários, especialidades, etc."
      backstory = "Você é um assistente que fornece informações sobre a clínica, você é cordial e prestativo."
      super().__init__(name=name, role=role, goal=goal, backstory=backstory, llm=llm)
      self.verbose = True
      self.tools = tools if tools is not None else []
