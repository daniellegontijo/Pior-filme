from django.apps import AppConfig

 # A classe AppConfig é utilzada para configurar alguns aspectos de uma aplicação, como seu nome, comportamento padrão e a configuração de campos de modelos.
class HelloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'intervalo_vencedor'

