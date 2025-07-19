import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

from src.tools.rag import RagTool
from src.agents.intent_agent import IntentAgent

load_dotenv()

llm = LLM(model="together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
          api_key=os.environ.get("TOGETHER_API_KEY"),
          base_url="https://api.together.xyz/v1"
        )

rag_tool = RagTool()

# Agente com a ferramenta
tagente = IntentAgent(
    llm=llm,
    tools=[rag_tool]
)

def test_intent_agent():
    """Testa a ferramenta Intent Agent na perspectiva de um agente CrewAI"""
    print("🧪 Testando Intent Agent via agente CrewAI...")

    test_queries = [
        "Olá bom dia",
        "Gostaria de marcar uma consulta",
        "Quais são os horários de funcionamento da clínica?",
        "Onde fica localizada a clínica?",
        # "Quais especialidades são oferecidas?",
        # "Qual o perfil profissional do Dr. Garcia?",
        # "Qual é o CRM do Dr. Garcia?",
        # "Qual é a formação acadêmica do Dr. Garcia?",
        # "Quais são os serviços oferecidos pela clínica?",
        "Meu dente de trás doi",
        "Olá bom dia, gostaria de marcar uma consulta",
        "Quanto é 2+2"
    ]

    for query in test_queries:
        print(f"\n📝 Consulta: {query}")
        task = Task(
            description=query,
            expected_output="Intenção da conversa.",
            agent=tagente
        )
        crew = Crew(
            agents=[tagente],
            tasks=[task],
            verbose=True
        )
        result = crew.kickoff()
        print(f"💬 Resultado: {result}")
        print("-" * 80)

if __name__ == "__main__":
    test_intent_agent()
