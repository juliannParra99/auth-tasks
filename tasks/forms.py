# django  creeara un formulario a partir de los datos que hay en la tabla creada en 'models.py'
from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        # variable que instancia clase que indica en que modelo va a estar basado mi formulario: es decir, en que tabla &modelo se van a persistir los datos de las tareas que se creen
        model = Task
        # fields indica las columnas que quiero utilizar de mi tabla( el usuario ya va a estar autenticado asique no hace falta): se genera formulario para enviar al frontend
        fields = ['title','description','important']
