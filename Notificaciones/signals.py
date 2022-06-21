from django.dispatch import Signal

notificar = Signal(providing_args=[
    'nivel'
    'usuario_id',
    'verbo', 
    'tiempo'
    ])