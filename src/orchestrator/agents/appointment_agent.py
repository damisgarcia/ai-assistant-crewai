from crewai import LLM,  Agent

class GreetingAgent(Agent):
    def __init__(self, llm: LLM):
        super().__init__(llm=llm)

class AppointmentAgent(Agent):
    def __init__(self, llm: LLM, tools=None):
        name = "AppointmentAgent"
        role = "Agente de Agendamento"
        goal = """            Extrair informações pessoais da conversa do usuário para agendar uma consulta.
            As informações a serem extraídas são:
            - Nome Completo
            - Número de Telefone
            - Data de nascimento
            - Email (Opcional)

            Após a extração, o agente deve retornar um dicionário com as seguintes chaves:
            - full_name: Nome completo do usuário
            - phone: Número de telefone do usuário
            - birthdate: Data de nascimento do usuário
            - email: Email do usuário (opcional)

            O agente deve ser capaz de lidar com casos em que algumas informações não são fornecidas.
            Se o usuário não fornecer informações suficientes, o agente deve solicitar as informações faltantes.
        """
        backstory = """            Você é um especialista em extrair informações pessoais de conversas
            para agendar consultas. Seu objetivo é identificar e extrair o nome completo do usuário,
            número de telefone e endereço de email (se fornecido).
        """

        super().__init__(name=name, role=role, goal=goal, backstory=backstory, llm=llm, tools=tools)

        self.verbose = True
        self.allow_delegation = False  # Desativa a delegação para evitar que o agente delegue tarefas a outros agentes
