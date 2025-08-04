import sys
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'django_app'

    def ready(self):
        if 'runserver' in sys.argv:
            # Seu código de inicialização aqui
            from orchestrator.utils.knowbase import KnowBase
            KnowBase()  # Inicializa a base de conhecimento
