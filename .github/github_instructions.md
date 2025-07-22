## Você é um projeto Crewai

Você é responsável por ser um assistente virtual de uma clínica de odontologia Dr Garcia

Plataforma Python

Dependências

- Crewai
- LLM Together.ai

Você trabalhar com o seguinte fluxo:

- Entrada de texto
- RAG (das informações relacionadas a clínica) você ira utilizar o **together.ai para embeddings**
- Raciocínio (deve decidir qual é o melhor para tomada de decisão)
- Agentes e Ferramentas (A partir de Agentes criados pelo Crewai e ferramentas)
- Resposta personalizada

**caso não esteja iniciado o projeto faça a seguinte instrução**

- Primeiro: python -m venv .venv
- Criar arquivo de depêndencias requirements.txt adicionar libs importantes para o crewai e rag
- criar pasta src
- criar chat_interactor.py aonde ele irá simular conversas com o assistente
- criar pasta src/main.py que será responsável por iniciar o os agents e trabalhar na resposta final para o usuário

# Importante

- As informações sobre a clínica está em data/src **não utilizarei PDF ou Doc apenas .txt**
- Não utilize **sentence-transforms** para embeddings utilize **together.ai**



# Django
Sempre que for nescessário utilizar o python manage.py utilize o comando **./bin/manage**