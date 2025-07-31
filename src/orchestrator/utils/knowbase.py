import os
import glob
import chromadb

import threading

class KnowBase:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, persist_dir=None, collection_name="garcia_clinic"):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(KnowBase, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, persist_dir=None, collection_name="garcia_clinic"):
        if getattr(self, '_initialized', False):
            return
        if persist_dir is None:
            persist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'chroma_db')
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection = self._get_or_create_collection()
        self._initialized = True

    def _get_or_create_collection(self):
        try:
            collection = self.client.get_collection(self.collection_name)
            print(f"📊 Coleção '{self.collection_name}' carregada.")
            return collection
        except Exception as e:
            print(f"⚠️ Coleção não encontrada: {e}. Criando nova coleção...")
            try:
                collection = self.client.create_collection(self.collection_name)
                print(f"📊 Coleção '{self.collection_name}' criada.")
                self.collection = collection  # Corrige o erro de atributo
                self.populate_from_data()
                return collection
            except Exception as ce:
                print(f"❌ Erro ao criar coleção: {ce}")
                return None

    def populate_from_data(self, data_dir=None):
        if data_dir is None:
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(parent_dir, 'data')
            print(f"📁 Diretório de dados escolhido: {data_dir}")
        if not os.path.exists(data_dir):
            print(f"⚠️ Pasta de dados não encontrada: {data_dir}")
            return
        txt_files = glob.glob(os.path.join(data_dir, '*.txt'))
        if not txt_files:
            print(f"⚠️ Nenhum arquivo .txt encontrado em {data_dir}")
            return
        documents, ids, metadatas = [], [], []
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

            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

            print(f"✅ {len(documents)} documentos adicionados à coleção!")

    def search(self, query, n_results=3):
        if self.collection is None:
            return {"documents": [], "metadatas": [], "error": "Base de conhecimento não inicializada"}
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return {
                "documents": results.get("documents", [[]])[0],
                "metadatas": results.get("metadatas", [[]])[0],
                "distances": results.get("distances", [[]])[0]
            }
        except Exception as e:
            return {"documents": [], "metadatas": [], "error": f"Erro na busca: {e}"}
