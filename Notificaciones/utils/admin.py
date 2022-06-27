from django.contrib import admin

class AbstractNotificacionAdmin(admin.ModelAdmin):
    raw_id_fields = ('usuario_id',)
    list_display = ('usuario_id', 'verbo', 'leido')
    list_filter = ('leido',)
    
    def get_queryset(self, request):
        qs = super(AbstractNotificacionAdmin, self).get_queryset(request)
        return qs.prefetch_related('usuario_id')