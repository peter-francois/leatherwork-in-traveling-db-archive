from django.http import HttpResponseForbidden

class BlockWordPressRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if '/wp-includes' in request.path or '/wp-content' in request.path or '/wp-config' in request.path or '/wp-admin' in request.path or '/wordpress' in request.path:
            # Retourner une réponse 403 (Forbidden)
            return HttpResponseForbidden("Accès interdit")
        
        # Si la requête n'est pas bloquée, continue le traitement normal
        response = self.get_response(request)
        return response