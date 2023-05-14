from django.contrib import admin
#aca voy a hacer que mi tabla SQL generada tenga acceso al panel de administrador
from .models import Task

#esta clsae es para mostrar por pantalla campos que son de solo lectura. En este caso el atributo 'created'
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Register your models here.
admin.site.register(Task, TaskAdmin)
