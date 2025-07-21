from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class SumToolInput(BaseModel):
    """Input schema for SumTool."""
    numbers: str = Field(..., description="Lista de números separados por vírgula para somar")

class SumTool(BaseTool):
    name: str = "math_sum"
    description: str = "Calcula a soma de uma lista de números separados por vírgula"
    args_schema: Type[BaseModel] = SumToolInput

    def _run(self, numbers: str) -> str:
        """Execute the tool."""
        try:
            # Converte a string em lista de números
            number_list = [float(x.strip()) for x in numbers.split(',')]
            result = sum(number_list)
            return f"A soma dos números {numbers} é: {result}"
        except ValueError as e:
            return f"Erro: Não foi possível converter '{numbers}' em números válidos. {e}"
        except Exception as e:
            return f"Erro ao calcular a soma: {e}"
