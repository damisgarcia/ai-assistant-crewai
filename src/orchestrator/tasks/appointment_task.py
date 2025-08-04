from crewai import Task

class AppointmentTasks:
    def extract_personal_info(self, agent, conversation_id: str):
        return Task(
            description=f"""
                Extraia o nome completo do usuário, número de telefone e, opcionalmente, o endereço de e-mail
                do contexto da conversa. Garanta que as informações extraídas sejam precisas e completas.
                Se alguma informação estiver faltando, declare que está faltando.

                O ID da conversa é: {conversation_id}

                Sua saída deve ser um objeto JSON com o seguinte formato:
                {{
                    "full_name": "[Nome Completo Extraído]",
                    "phone": "[Número de Telefone Extraído]",
                    "email": "[Email Extraído ou nulo se não fornecido]",
                    "birthdate": "[Data de Nascimento Extraída ou nulo se não fornecido]",
                }}

                Se o usuário não fornecer informações suficientes, o agente deve solicitar as informações faltantes passo a passo seguindo
                esta ordem: telefone, nome completo, data de nascimento e email.
                """,
            agent=agent,
            expected_output="Um objeto JSON nome completo, telefone, email e data de nascimento.",
        )

    def ask_for_missing_info(self, agent, missing_info):
        return Task(
            description="""
                Solicite ao usuário as informações faltantes: {missing_info}.
                Certifique-se de que a solicitação seja clara e direta.
                """,
            agent=agent,
            expected_output="Mensagem solicitando uma informação faltante seguindo está ordem de prioridade ().",
        )

