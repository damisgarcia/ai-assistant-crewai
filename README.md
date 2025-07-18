# Assistente Virtual - Clínica Dr. Garcia

Assistente virtual desenvolvido com CrewAI e Together.ai para a Clínica Odontológica Dr. Garcia.

## Funcionalidades

- **RAG (Retrieval Augmented Generation)** com embeddings do Together.ai
- **Agentes especializados** usando CrewAI
- **Base de conhecimento** com informações da clínica
- **Interface de chat** interativa

## Configuração

### 1. Ambiente Virtual

O ambiente virtual já está configurado em `.venv/`

### 2. Dependências

As dependências já foram instaladas:

- CrewAI
- Together.ai
- ChromaDB
- LangChain
- Streamlit

### 3. Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da API do Together.ai:

```
TOGETHER_API_KEY=sua_chave_aqui
```

## Estrutura do Projeto

```
├── data/                     # Informações da clínica (arquivos .txt)
│   ├── address.txt          # Endereço e contato
│   ├── business-hours.txt   # Horários de funcionamento
│   ├── professional-profile.txt # Perfil do Dr. Garcia
│   ├── social-media.txt     # Redes sociais
│   └── specialties.txt      # Especialidades oferecidas
├── src/
│   └── main.py             # Sistema principal com agentes
├── chat_interactor.py      # Interface de chat
├── requirements.txt        # Dependências
└── .env.example           # Exemplo de configuração
```

## Como Usar

### 1. Testar o Sistema Principal

```bash
/home/damisgarcia/lab/ai-assistant-garcia-consultancy-crewai/.venv/bin/python src/main.py
```

### 2. Usar o Chat Interativo

```bash
/home/damisgarcia/lab/ai-assistant-garcia-consultancy-crewai/.venv/bin/python chat_interactor.py
```

## Fluxo do Sistema

1. **Entrada de texto** - Recebe a pergunta do usuário
2. **RAG** - Busca informações relevantes usando embeddings do Together.ai
3. **Raciocínio** - Decide qual agente é mais adequado
4. **Agentes e Ferramentas** - Processa usando CrewAI
5. **Resposta personalizada** - Retorna resposta contextualizada

## Próximos Passos

- [ ] Implementar agentes CrewAI especializados
- [ ] Adicionar interface web com Streamlit
- [ ] Implementar sistema de agendamento
- [ ] Adicionar métricas e logs
- [ ] Integração com WhatsApp/Telegram

## Tecnologias

- **Python 3.12+**
- **CrewAI** - Framework de agentes
- **Together.ai** - LLM e embeddings
- **ChromaDB** - Base de dados vetorial
- **LangChain** - Framework para LLM
- **Streamlit** - Interface web
