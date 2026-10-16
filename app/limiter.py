from slowapi import Limiter
from slowapi.util import get_remote_address

# Inicialización de Rate Limiter basado en IP del cliente
limiter = Limiter(key_func=get_remote_address)