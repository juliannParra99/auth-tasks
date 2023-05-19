from django.shortcuts import render, redirect
# userCreationForm es para crear un usuario y AuthenticationForm es para comprobar si el usurio existe.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
#importo el modelo de  las tareas: permite interactuar con la DB y hacer consultas
from .models import Task

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
    #esto va a devolver  las tareas que estan en la DB, y ene ste caso, donde las tareas son del usuario user, y donde  datecompleted__isnull = true, osea las tareas que no han sido completadas: con esto puedo mostrar al usuario las tareas que le faltan hacer; tambien podria mostrar las que ya completo
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull= True )

    return render(request, 'tasks.html', {
        'tasks': tasks
    })


def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            "form": TaskForm,
        })
    else:
        try:
            
            form = TaskForm(request.POST)

            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                "form": TaskForm,
                "error": 'Please provide valid data'
            })


def signout(request):
    logout(request)
    return redirect('home')


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
