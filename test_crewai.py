import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

from src.tools.math import SumTool

load_dotenv()

llm = LLM(model="together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
          api_key=os.environ.get("TOGETHER_API_KEY"),
          base_url="https://api.together.xyz/v1"
        )

sum_tool = SumTool()

# Agente com a ferramenta
agente = Agent(
    name='MathAgent',
    role='Professor de Matemática',
    goal='Ira receber uma lista de números e calcular o somatório.',
    backstory='Especialista em Matemática, capaz de realizar cálculos complexos.',
    verbose=True,
    tools=[sum_tool],
    llm=llm,
)

# Task que espera usar a ferramenta
task = Task(
    description="Calcule o somatório das vendas usando os seguintes dados: 100,200,300,400,500.",
    expected_output="Valor do somatório das vendas.",
    agent=agente
)

# Crew
crew = Crew(
    agents=[agente],
    tasks=[task],
    verbose=True
)

crew.kickoff()
