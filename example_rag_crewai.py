"""
Exemplo de uso da ferramenta RAG com CrewAI
"""
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

from src.tools.rag import RagTool

load_dotenv()

# Configuração do LLM
llm = LLM(
    model="together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
    api_key=os.environ.get("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1"
)

# Instância da ferramenta RAG
rag_tool = RagTool()

# Agente especializado em atendimento da clínica
atendimento_agent = Agent(
    name='AtendimentoAgent',
    role='Assistente de Atendimento da Clínica Dr. Garcia',
    goal='Fornecer informações precisas sobre a clínica usando a base de conhecimento.',
    backstory='Você é um assistente virtual especializado em atendimento ao paciente da Clínica Dr. Garcia. Use sempre a base de conhecimento para fornecer informações precisas.',
    verbose=True,
    tools=[rag_tool],
    llm=llm,
)

# Task que usa a ferramenta RAG
task = Task(
    description="Um paciente está perguntando sobre os horários de funcionamento da clínica. Use a ferramenta de busca na base de conhecimento para encontrar essas informações e responda de forma clara e educada.",
    expected_output="Informações completas sobre os horários de funcionamento da clínica.",
    agent=atendimento_agent
)

# Crew
crew = Crew(
    agents=[atendimento_agent],
    tasks=[task],
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Executando exemplo com ferramenta RAG...")
    result = crew.kickoff()
    print(f"\n✅ Resultado final: {result}")
