# teste_pior_filme/middleware.py

class CloseConnectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Código para fechar a conexão ou qualquer outra lógica
        return response
