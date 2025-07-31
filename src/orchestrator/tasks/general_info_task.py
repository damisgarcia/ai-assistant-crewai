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

