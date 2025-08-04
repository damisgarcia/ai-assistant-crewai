import os
import json

from crewai import Task, LLM

from orchestrator.utils.knowbase import KnowBase

from orchestrator.agents import IntentAgent, GreetingAgent, InfoAgent, FailAgent, AppointmentAgent
from orchestrator.tools import RagTool, FetchUserMessageTool, ChangeStatusRegisteringContactTool
from orchestrator.tasks import GreetingTask, GeneralInfoTask, UnknownTask, AppointmentTasks


import threading

class Orchestrator:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        # Initialize the knowledge base
        self.knowbase = KnowBase()

        # Initialize tools and agents
        self.rag_tool = RagTool()

        self.llm = LLM(
            model="together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
            api_key=os.environ.get("TOGETHER_API_KEY"),
            base_url="https://api.together.xyz/v1"
        )

        self.intent_agent = IntentAgent(llm=self.llm)
        self.greeting_agent = GreetingAgent(llm=self.llm, tools=[self.rag_tool])
        self.info_agent = InfoAgent(llm=self.llm, tools=[self.rag_tool])
        self.fail_agent = FailAgent(llm=self.llm)

        self.appointment_agent = AppointmentAgent(llm=self.llm, tools=[
            self.rag_tool,
            ChangeStatusRegisteringContactTool(),
            FetchUserMessageTool(),
        ])

    def process_query(self, query, conversation_id=None):
        task_classification = Task(
            description=query,
            expected_output="Intenção da conversa.",
            agent=self.intent_agent
        )

        intent = task_classification.execute_sync()

        if intent.raw == "greeting":
            task = GreetingTask(query=query, agent=self.greeting_agent, context=[task_classification])
        elif intent.raw == "info":
            task = GeneralInfoTask(query=query, agent=self.info_agent, context=[task_classification])
        elif intent.raw == "appointment":
            personal_info_task = AppointmentTasks().extract_personal_info(self.appointment_agent, conversation_id).execute_sync()
            try:
                contact_json = json.loads(personal_info_task.raw)
                empty_fields = [key for key, value in contact_json.items() if not value]

                if len(empty_fields) > 0:
                    task = AppointmentTasks().ask_for_missing_info(self.appointment_agent, empty_fields)
                else:
                    task = Task(
                        name="Tarefa de Confirmação de Agendamento",
                        description="Confirme o agendamento com as informações de contato fornecidas.",
                        expected_output="Mensagem de confirmação do agendamento.",
                        agent=self.appointment_agent,
                        context=[task_classification, personal_info_task]
                    )

            except json.JSONDecodeError:
                task = UnknownTask(query=query, agent=self.fail_agent)
        else:
            task = UnknownTask(query=query, agent=self.fail_agent)

        result = task.execute_sync()

        return result.raw
