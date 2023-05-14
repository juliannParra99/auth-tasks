# con esto le voy a indicar  django que cree un formulario a partir de los datos que hay en la tabla que creamos en 'models.py'
from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        # aca creo una variable que va indicar en que modelo va a estar basado mi formulario: es decir, en que tabla(modelo) se van a persistir los datos de las tareas que cree (po que podemos tener varias tablas)
        model = Task
        #en fields indico las columnas que quiero utilizar de mi tabla: title, description  e impotant (los otros no, el usuario ya va a estar autenticado asique no hace falta) : con esto ya tengo un formulario que puedo empezar a enviar al frontend
        fields = ['title','description','important']
