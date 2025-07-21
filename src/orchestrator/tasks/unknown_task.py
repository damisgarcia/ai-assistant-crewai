from crewai import Task

class UnknownTask(Task):
    def __init__(self, name="Unknown Task", query="", agent=None, context=None):
        description=f"A mensagem não foi compreendida, pergunte como posso ajudar?"
        expected_output="Mensagem pedindo reformulação ou transferindo para um humano."
        agent=agent
        context=context

        super().__init__(
            name=name, 
            description=description, 
            expected_output=expected_output, 
            agent=agent, 
            context=context
        )

