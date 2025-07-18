import os
from crewai import LLM, Task, Agent, Crew

class DecideAgent(Agent):
    role = "Decide Agent"

    def __init__(self, name="DecideAgent"):
        super().__init__(name=name)
        self.llm = LLM(model_name=os.getenv("TOGETHER_MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"))
        self.goal = "Baseado no input do usuário, decida a próxima ação a ser tomada."
        self.backstory = "Você é um agente que decide a próxima ação com base na descrição da tarefa fornecida pelo usuário. Use seu conhecimento e raciocínio para determinar o melhor curso de ação."
        self.verbose = True
