## Gemini Added Memories

- O projeto está sendo desenvolvido com Python Django e Nuxt3
- Você é responsável por criar um sistema multi-agentes para trabalhar como um assistente virtual de uma clínica de odontologia Dr Garcia
- Sempre que for criar um agente utilize como base este template:

```
from crewai import LLM,  Agent

class GreetingAgent(Agent):
  def __init__(self, name="GreetingAgent", role="Agente de Boas-Vindas", llm=LLM, tools=None):
      goal = "Responder com uma mensagem de boas-vindas passe informações básicas da clínica."
      backstory = "Você é um atendente cordial e prestativo."
      super().__init__(name=name, role=role, goal=goal, backstory=backstory, llm=llm)
      self.verbose = False  # Desativa o modo verbose para evitar logs excessivos
      self.tools = tools if tools is not None else []

```

- Sempre que for criar uma task utilize como base este template:

```
from crewai import Task

class GeneralInfoTask(Task):
    def __init__(self, name="General Info Task", query="", agent=None, context=None):
        description=f"Responda à solicitação de informação: {query}"
        expected_output="Mensagem com a informação solicitada ou próxima no formato **Markdown**."
        agent=agent
        context=context

        super().__init__(
            name=name,
            description=description,
            expected_output=expected_output,
            agent=agent,
            context=context
        )

```

- Sempre que for nescessário utilizar o python manage.py utilize o comando **./bin/manage**
