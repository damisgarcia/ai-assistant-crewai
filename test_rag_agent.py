"""
Teste da ferramenta RAG integrada a um agente CrewAI
"""
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

from src.tools.rag import RagTool

load_dotenv()

# Configuração do LLM (ajuste conforme necessário)
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

def test_rag_agent():
    """Testa a ferramenta RAG na perspectiva de um agente CrewAI"""
    print("🧪 Testando ferramenta RAG via agente CrewAI...")

    test_queries = [
        "Quais são os horários de funcionamento da clínica?",
        "Onde fica localizada a clínica?",
        "Quais especialidades são oferecidas?",
        "Qual o perfil profissional do Dr. Garcia?"
    ]

    for query in test_queries:
        print(f"\n📝 Consulta: {query}")
        task = Task(
            description=query,
            expected_output="Informação precisa e clara sobre a clínica.",
            agent=atendimento_agent
        )
        crew = Crew(
            agents=[atendimento_agent],
            tasks=[task],
            verbose=True
        )
        result = crew.kickoff()
        print(f"💬 Resultado: {result}")
        print("-" * 80)

if __name__ == "__main__":
    test_rag_agent()
