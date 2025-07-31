import os
from dotenv import load_dotenv
from crewai import Task, LLM

from src.orchestrator.tools import RagTool
from src.orchestrator.agents import FailAgent, GreetingAgent, InfoAgent, IntentAgent
from src.orchestrator.tasks import GreetingTask, UnknownTask, GeneralInfoTask

load_dotenv()

llm = LLM(
    model="together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
    api_key=os.environ.get("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1"
)

rag_tool = RagTool()

# Agente com a ferramenta
intent_agent = IntentAgent(llm=llm)

greeting_assistant = GreetingAgent(llm=llm, tools=[rag_tool])
info_assistant = InfoAgent(llm=llm, tools=[rag_tool])
fail_assistant = FailAgent(llm=llm)

def test_intent_agent():
    """Testa a ferramenta Intent Agent na perspectiva de um agente CrewAI"""
    print("🧪 Testando Intent Agent via agente CrewAI...")

    test_queries = [
        "Olá bom dia",
        # "Gostaria de marcar uma consulta",
        # "Quais são os horários de funcionamento da clínica?",
        "Onde fica localizada a clínica?",
        # "Quais especialidades são oferecidas?",
        # "Qual o perfil profissional do Dr. Garcia?",
        # "Qual é o CRM do Dr. Garcia?",
        # "Qual é a formação acadêmica do Dr. Garcia?",
        # "Quais são os serviços oferecidos pela clínica?",
        # "Meu dente de trás doi",
        # "Olá bom dia, gostaria de marcar uma consulta",
        "Quanto é 2+2"
    ]

    for query in test_queries:
        print(f"\n📝 Consulta: {query}")
        task_classification = Task(
            description=query,
            expected_output="Intenção da conversa.",
            agent=intent_agent
        )

        intent = task_classification.execute_sync()

        if intent.raw == "greeting":
            task = GreetingTask(query=query, agent=greeting_assistant, context=[task_classification])
        elif intent.raw == "info":
            task = GeneralInfoTask(query=query, agent=info_assistant, context=[task_classification])
        else:
            task = UnknownTask(query=query, agent=fail_assistant)

        result = task.execute_sync()
        print(f"💬 Resultado: {result}")
        print("-" * 80)

if __name__ == "__main__":
    test_intent_agent()
