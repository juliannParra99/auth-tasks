from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#  Esta clase va a crear una tabla de sql
# django va  a crear la tabla; se le indico que tipo de dato quiero que sea las columnas; las columnas son los atributos de la clase
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #esto muestra el nombre de la tarea y no solo un objeto;
    #  self es como una referencia a la clase del modelo
    def __str__(self):
        return self.title + ' -by ' + self.user.username


