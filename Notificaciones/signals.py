from django.dispatch import Signal

notificar = Signal(providing_args=[
    'usuario_id',
    'actor',
    'verbo', 
    'tiempo',
    'direct'
    ])