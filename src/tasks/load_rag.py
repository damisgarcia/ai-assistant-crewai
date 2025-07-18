import os
from typing import Dict, Any, List
import chromadb
from together import Together
import glob

from crewai import LLM, Task

class LoadRag(Task):
    def __init__(self, name="LoadRagTask", role="RAG Loader"):
        super().__init__(name=name, role=role)

        self.llm = LLM(model_name=os.getenv("TOGETHER_MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"))
        self.goal = "Carregar e inicializar o sistema de Recuperação de Informações (RAG) com os dados necessários."
        self.backstory = "Você é um agente responsável por carregar e configurar o sistema RAG com os dados necessários para responder às consultas dos usuários."
        self.verbose = True
        self.together_client = Together(api_key=os.getenv('TOGETHER_API_KEY'))

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

    def run(self):
      """
      Configura a base de conhecimento RAG com ChromaDB e Together.ai embeddings
      """
      print("📚 Configurando base de conhecimento...")

      try:
          # Inicializa ChromaDB com configuração persistente
          persist_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'chroma_db')
          chroma_client = chromadb.PersistentClient(path=persist_directory)

          # Nome da coleção
          collection_name = "garcia_clinic"

          # Verifica se a coleção já existe
          existing_collections = [col.name for col in chroma_client.list_collections()]

          if collection_name in existing_collections:
              self.collection = chroma_client.get_collection(collection_name)
              print("📊 Coleção existente carregada")

              # Verifica se há documentos na coleção
              count = self.collection.count()
              if count > 0:
                  print(f"📄 {count} documentos encontrados na coleção")
                  return True
              else:
                  print("📊 Coleção vazia, recarregando documentos...")
                  # Deleta a coleção vazia e recria
                  chroma_client.delete_collection(collection_name)

          # Cria nova coleção
          collection = chroma_client.create_collection(collection_name)
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
          collection.add(
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
