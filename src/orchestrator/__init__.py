import os

from crewai import Task, LLM

from orchestrator.utils.knowbase import KnowBase

from orchestrator.agents import IntentAgent, GreetingAgent, InfoAgent, FailAgent
from orchestrator.tools import RagTool
from orchestrator.tasks import GreetingTask, GeneralInfoTask, UnknownTask


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

    def process_query(self, query):
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
        else:
            task = UnknownTask(query=query, agent=self.fail_agent)

        result = task.execute_sync()

        return result.raw
