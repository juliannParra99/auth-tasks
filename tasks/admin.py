from django.contrib import admin
#aca voy a hacer que mi tabla SQL generada tenga acceso al panel de administrador, para qu asi pueda crear mis tareas y se guarden en la tabla. para lo cual traigo mi modelo llamado  'Tasks'
from .models import Task

#esta clsae es para mostrar por pantalla campos que son de solo lectura. En este caso el atributo 'created': que muestra las tareas que se han creado y que no puede ser modificado por que ese campo es de solo lectura
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Register your models here.
admin.site.register(Task, TaskAdmin)
