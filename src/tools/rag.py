"""
RAG Tool - Ferramenta para buscar informações na base de conhecimento da clínica
"""
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from dotenv import load_dotenv
from src.utils.knowbase import KnowBase

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

    def _run(self, query: str) -> str:
        """Execute a busca na base de conhecimento"""
        try:
            knowbase = KnowBase()
            search_results = knowbase.search(query=query)

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
