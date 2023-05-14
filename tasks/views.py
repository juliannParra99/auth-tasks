from django.shortcuts import render, redirect
# userCreationForm es para crear un usuario y AuthenticationForm es para comprobar si el usurio existe.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm

# Create your views here.


def home(request):
    return render(request, 'home.html')

# esta funcion es la que va a permitir enviar el archivo que va a contener el formulario


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    "form": UserCreationForm(),
                    "error": "Username already exists"
                })
        return render(request, 'signup.html', {
            "form": UserCreationForm(),
            "error": "Password do not match"
        })


def tasks(request):
    return render(request, 'tasks.html')


def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            "form": TaskForm,
        })
    else:
        try:
            #con esto ya puedo guardar las tareas desde mi formulario: lo puedo ver desde
            #el panel de administrador. Con esto  se crea una especie de formulario con los datos que yo le estoy enviando para crear la tarea
            form = TaskForm(request.POST)
            #print(form)#esto es para que se vea en el ejemplo que la tarea se muestra en la consola; lo comento pq no es seguro

            #el formulario se crea para guardar los datos.
            new_task = form.save(commit=False)
            #el request.user es por que el modelo de nuestra tabla exigue un usuario que maneje las tareas
            new_task.user = request.user
            #esto va a generar un dato dentro de la DB
            new_task.save()
            #una vez guardado el dato redirije a la pagina tasks
            return redirect('tasks')
        #para comprobar si es un error, y consideremos cuando lo es
        except ValueError:
            return render(request, 'create_task.html', {
                "form": TaskForm,
                "error": 'Please provide valid data'
            })


def signout(request):
    logout(request)
    return redirect('home')

# metodo para que el usuario se pueda autenticas (acceda a sus datos si tiene una cuenta ya creada)
# si la solicitud a esa url es get muestro el formulario, si no, si es una solicutd post, verifico
# si el usuario es none, osea si no existe, mando el error con el formulario, si existe lo envio a la
# pagina 'tasks' y guardo su session


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': " Username or password is incorrect"
            })
        else:
            login(request, user)
            return redirect('tasks')
