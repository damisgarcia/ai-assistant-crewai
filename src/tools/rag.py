"""
RAG Tool - Ferramenta para buscar informações na base de conhecimento da clínica
"""
import os
import glob
from typing import Type, List, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import chromadb
from together import Together
from dotenv import load_dotenv

load_dotenv()

class RagToolInput(BaseModel):
    """Input schema for RagTool."""
    query: str = Field(..., description="Pergunta ou consulta para buscar informações sobre a clínica")


class RagTool(BaseTool):
    name: str = "clinic_knowledge_search"
    description: str = "Busca informações na base de conhecimento da Clínica Dr. Garcia usando RAG com Together.ai embeddings"
    args_schema: Type[BaseModel] = RagToolInput

    def __init__(self):
        super().__init__()
        self._together_client = None
        self._chroma_client = None
        self._collection = None
        self._initialize_rag_system()

    def _initialize_rag_system(self):
        """Inicializa o sistema RAG"""
        try:
            if self._together_client is None:
                self._together_client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
            if self._chroma_client is None:
                persist_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'chroma_db')
                self._chroma_client = chromadb.PersistentClient(path=persist_directory)
            if self._collection is None:
                try:
                    self._collection = self._chroma_client.get_collection("garcia_clinic")
                    print("📊 Coleção RAG carregada para a ferramenta")
                except Exception as e:
                    print(f"⚠️ Coleção não encontrada ou erro ao carregar: {type(e).__name__}: {e}")
                    # Tenta criar a coleção se não existir
                    try:
                        self._collection = self._chroma_client.create_collection("garcia_clinic")
                        print("📊 Coleção criada para a ferramenta")
                        # Alimenta a coleção com os documentos da pasta data/
                        self._populate_collection_from_data()
                    except Exception as ce:
                        print(f"❌ Erro ao criar coleção: {type(ce).__name__}: {ce}")
                        self._collection = None
        except Exception as e:
            print(f"❌ Erro ao inicializar sistema RAG na ferramenta: {e}")

    def _populate_collection_from_data(self):
        """Popula a coleção com os documentos da pasta data/"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')

        if not os.path.exists(data_dir):
            print(f"⚠️ Pasta de dados não encontrada: {data_dir}")
            return

        txt_files = glob.glob(os.path.join(data_dir, '*.txt'))
        if not txt_files:
            print(f"⚠️ Nenhum arquivo .txt encontrado em {data_dir}")
            return
        documents = []
        ids = []
        metadatas = []

        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append(content)
                    ids.append(os.path.basename(file_path))
                    metadatas.append({'source': file_path})
            except Exception as e:
                print(f"❌ Erro ao ler {file_path}: {e}")

        if documents:
            print(f"🔄 Gerando embeddings para {len(documents)} documentos...")
            embeddings = self.get_embeddings(documents)
            if embeddings:
                self._collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"✅ {len(documents)} documentos adicionados à coleção!")
            else:
                print("❌ Falha ao gerar embeddings para os documentos.")

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        self._initialize_rag_system()
        """Gera embeddings usando Together.ai"""
        try:
            embeddings = []
            for text in texts:
                response = self._together_client.embeddings.create(
                    input=text,
                    model=os.environ.get('TOGETHER_EMBEDDING_MODEL', 'togethercomputer/m2-bert-80M-32k-retrieval')
                )
                embeddings.append(response.data[0].embedding)
            return embeddings
        except Exception as e:
            print(f"❌ Erro ao gerar embeddings: {e}")
            return []

    def search_knowledge_base(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        self._initialize_rag_system()
        """Busca informações relevantes na base de conhecimento"""
        try:
            if self._collection is None:
                return {"documents": [], "metadatas": [], "error": "Base de conhecimento não inicializada"}
            query_embeddings = self.get_embeddings([query])
            if not query_embeddings:
                return {"documents": [], "metadatas": [], "error": "Falha ao gerar embedding da query"}
            results = self._collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results
            )
            return {
                "documents": results.get("documents", [[]])[0],
                "metadatas": results.get("metadatas", [[]])[0],
                "distances": results.get("distances", [[]])[0]
            }
        except Exception as e:
            return {"documents": [], "metadatas": [], "error": f"Erro na busca: {e}"}

    def _run(self, query: str) -> str:
        """Execute a busca na base de conhecimento"""
        try:
            # Busca informações relevantes
            search_results = self.search_knowledge_base(query)

            # Verifica se houve erro
            if "error" in search_results:
                return f"Erro ao buscar informações: {search_results['error']}"

            # Monta a resposta com as informações encontradas
            documents = search_results.get("documents", [])

            if not documents:
                return "Nenhuma informação relevante encontrada na base de conhecimento da clínica."

            # Formata a resposta
            response = "Informações encontradas na base de conhecimento da Clínica Dr. Garcia:\n\n"

            for i, doc in enumerate(documents, 1):
                response += f"📄 Informação {i}:\n{doc}\n\n"

            return response.strip()

        except Exception as e:
            return f"Erro ao executar busca na base de conhecimento: {e}"
