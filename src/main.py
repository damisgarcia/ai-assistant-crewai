"""
Main.py - Responsável por iniciar os agentes e trabalhar na resposta final para o usuário
Sistema de Assistente Virtual para Clínica Dr. Garcia usando CrewAI e Together.ai
"""
import os
import sys
from typing import Dict, Any, List
from dotenv import load_dotenv
import chromadb
from together import Together
import glob

# Carrega variáveis de ambiente
load_dotenv()


class GarciaClinicAssistant:
    """
    Assistente Virtual principal da Clínica Dr. Garcia
    Coordena agentes CrewAI e sistema RAG com Together.ai
    """

    def __init__(self):
        """Inicializa o assistente e seus componentes"""
        self.together_client = None
        self.knowledge_base = None
        self.chroma_client = None
        self.collection = None
        self.agents = {}
        self.crew = None
        self.setup_environment()

    def setup_environment(self):
        """Configura o ambiente e variáveis necessárias"""
        # Verifica se as variáveis de ambiente necessárias estão definidas
        required_env_vars = ['TOGETHER_API_KEY']
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]

        if missing_vars:
            print(f"⚠️  Variáveis de ambiente faltando: {', '.join(missing_vars)}")
            print("Por favor, configure essas variáveis no arquivo .env")
            return False

        # Inicializa o cliente Together.ai
        try:
            self.together_client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
            print("✅ Cliente Together.ai inicializado")
        except Exception as e:
            print(f"❌ Erro ao inicializar Together.ai: {e}")
            return False

        return True

    def load_clinic_data(self) -> List[Dict[str, str]]:
        """
        Carrega todos os arquivos .txt da pasta data/
        """
        # Corrige o caminho para a pasta data (está um nível acima de src/)
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        txt_files = glob.glob(os.path.join(data_path, '*.txt'))

        documents = []
        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    documents.append({
                        'id': os.path.basename(file_path),
                        'content': content,
                        'source': file_path
                    })
                    print(f"📄 Carregado: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"❌ Erro ao carregar {file_path}: {e}")

        return documents

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Gera embeddings usando Together.ai
        """
        try:
            embeddings = []
            for text in texts:
                response = self.together_client.embeddings.create(
                    input=text,
                    model=os.environ.get('TOGETHER_EMBEDDING_MODEL', 'togethercomputer/m2-bert-80M-32k-retrieval')
                )
                embeddings.append(response.data[0].embedding)
            return embeddings
        except Exception as e:
            print(f"❌ Erro ao gerar embeddings: {e}")
            return []

    def setup_knowledge_base(self):
        """
        Configura a base de conhecimento RAG com ChromaDB e Together.ai embeddings
        """
        print("📚 Configurando base de conhecimento...")

        try:
            # Inicializa ChromaDB com configuração persistente
            persist_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'chroma_db')
            self.chroma_client = chromadb.PersistentClient(path=persist_directory)

            # Nome da coleção
            collection_name = "garcia_clinic"

            # Verifica se a coleção já existe
            existing_collections = [col.name for col in self.chroma_client.list_collections()]

            if collection_name in existing_collections:
                self.collection = self.chroma_client.get_collection(collection_name)
                print("📊 Coleção existente carregada")

                # Verifica se há documentos na coleção
                count = self.collection.count()
                if count > 0:
                    print(f"📄 {count} documentos encontrados na coleção")
                    return True
                else:
                    print("📊 Coleção vazia, recarregando documentos...")
                    # Deleta a coleção vazia e recria
                    self.chroma_client.delete_collection(collection_name)

            # Cria nova coleção
            self.collection = self.chroma_client.create_collection(collection_name)
            print("📊 Nova coleção criada")

            # Carrega documentos da clínica
            documents = self.load_clinic_data()

            if not documents:
                print("❌ Nenhum documento encontrado na pasta data/")
                return False

            # Prepara dados para inserção
            ids = [doc['id'] for doc in documents]
            contents = [doc['content'] for doc in documents]
            metadatas = [{'source': doc['source']} for doc in documents]

            # Gera embeddings usando Together.ai
            print("🔄 Gerando embeddings...")
            embeddings = self.get_embeddings(contents)

            if not embeddings:
                print("❌ Falha ao gerar embeddings")
                return False

            # Adiciona à coleção
            self.collection.add(
                embeddings=embeddings,
                documents=contents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ {len(documents)} documentos indexados na base de conhecimento")
            return True

        except Exception as e:
            print(f"❌ Erro ao configurar base de conhecimento: {e}")
            return False

    def search_knowledge_base(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        """
        Busca informações relevantes na base de conhecimento usando Together.ai embeddings
        """
        try:
            # Verifica se a coleção foi inicializada
            if self.collection is None:
                print("❌ Coleção não inicializada")
                return {"documents": [], "metadatas": []}

            # Gera embedding da query
            query_embeddings = self.get_embeddings([query])

            if not query_embeddings:
                print("❌ Falha ao gerar embedding da query")
                return {"documents": [], "metadatas": []}

            # Busca documentos similares
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results
            )

            return {
                "documents": results.get("documents", [[]])[0],
                "metadatas": results.get("metadatas", [[]])[0],
                "distances": results.get("distances", [[]])[0]
            }

        except Exception as e:
            print(f"❌ Erro na busca RAG: {e}")
            return {"documents": [], "metadatas": []}

    def create_agents(self):
        """
        Cria os agentes CrewAI especializados
        """
        # TODO: Implementar agentes CrewAI
        print("🤖 Criando agentes especializados...")
        pass

    def setup_crew(self):
        """
        Configura o crew (equipe) de agentes
        """
        # TODO: Implementar crew com tarefas específicas
        print("👥 Configurando equipe de agentes...")
        pass

    def decide_agent(self, query: str, context: Dict[str, Any]) -> str:
        """
        Decide qual agente é mais adequado para responder a consulta
        """
        query_lower = query.lower()

        # Lógica simples de decisão baseada em palavras-chave
        if any(word in query_lower for word in ['agendar', 'marcar', 'consulta', 'horário']):
            return "agendamento"
        elif any(word in query_lower for word in ['preço', 'valor', 'custo', 'quanto']):
            return "financeiro"
        elif any(word in query_lower for word in ['especialidade', 'tratamento', 'procedimento']):
            return "clinico"
        elif any(word in query_lower for word in ['endereço', 'localização', 'onde']):
            return "informacoes"
        else:
            return "atendimento"

    def generate_response_with_together(self, query: str, context: str) -> str:
        """
        Gera resposta usando Together.ai LLM
        """
        try:
            prompt = f"""Você é um assistente virtual da Clínica Odontológica Dr. Garcia.

Contexto da clínica:
{context}

Pergunta do paciente: {query}

Responda de forma educada, profissional e informativa. Use as informações do contexto para dar uma resposta precisa. Se não souber algo, seja honesto e sugira entrar em contato com a clínica."""

            response = self.together_client.chat.completions.create(
                model=os.environ.get('TOGETHER_MODEL_NAME', 'meta-llama/Llama-3.3-70B-Instruct-Turbo-Free'),
                messages=[
                    {"role": "system", "content": "Você é um assistente virtual profissional de uma clínica odontológica."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ Erro ao gerar resposta: {e}")
            return "Desculpe, ocorreu um erro interno. Por favor, entre em contato conosco pelo telefone (11) 3456-7890."

    def process_user_query(self, query: str) -> str:
        """
        Processa a consulta do usuário através do fluxo:
        Entrada -> RAG -> Raciocínio -> Agentes -> Resposta personalizada
        """
        try:
            print(f"🔍 Processando consulta: {query}")

            # 1. Busca RAG na base de conhecimento
            search_results = self.search_knowledge_base(query)

            # 2. Monta contexto relevante
            context = "\n".join(search_results.get("documents", []))

            # 3. Raciocínio para decidir qual agente usar
            agent_type = self.decide_agent(query, search_results)
            print(f"🎯 Agente selecionado: {agent_type}")

            # 4. Gera resposta usando Together.ai
            response = self.generate_response_with_together(query, context)

            return response

        except Exception as e:
            print(f"❌ Erro ao processar consulta: {e}")
            return "Desculpe, ocorreu um erro interno. Por favor, tente novamente ou entre em contato conosco."

    def initialize_system(self):
        """
        Inicializa todo o sistema do assistente
        """
        print("🚀 Inicializando Assistente Virtual da Clínica Dr. Garcia...")

        try:
            if not self.setup_environment():
                return False

            if not self.setup_knowledge_base():
                return False

            self.create_agents()
            self.setup_crew()

            print("✅ Sistema inicializado com sucesso!")
            return True

        except Exception as e:
            print(f"❌ Erro na inicialização: {e}")
            return False


def main():
    """Função principal"""
    assistant = GarciaClinicAssistant()

    if assistant.initialize_system():
        print("Sistema pronto para uso!")

        # Exemplo de uso
        test_queries = [
            "Quais são os horários de funcionamento da clínica?",
            "Quais especialidades vocês oferecem?",
            "Onde fica localizada a clínica?"
        ]

        for query in test_queries:
            print(f"\n📝 Teste: {query}")
            response = assistant.process_user_query(query)
            print(f"💬 Resposta: {response}")
    else:
        print("Falha na inicialização do sistema.")


if __name__ == "__main__":
    main()
