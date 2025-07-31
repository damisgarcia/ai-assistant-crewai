from crewai import Task

class GreetingTask(Task):
    def __init__(self, name="Greeting Task", query="", agent=None, context=None):
        description = f"Responda educadamente à saudação: '{query}'"
        expected_output = "Mensagem de boas-vindas no formato **Markdown**."
        agent = agent
        context = context

        super().__init__(
            name=name,
            description=description,
            expected_output=expected_output,
            agent=agent,
            context=context
        )

