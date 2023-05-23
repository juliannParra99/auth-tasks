from django.shortcuts import render, redirect, get_object_or_404
# userCreationForm es para crear un usuario y AuthenticationForm es para comprobar si el usurio existe.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone

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

    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)

    return render(request, 'tasks.html', {
        'tasks': tasks,
        'title': 'Pending Tasks'
    })

# va a mostrar las tareas que ya han sido completadas
def tasks_completed(request):
    #  lo que cambia aca es que el datecompleted_isnull= False, por lo que va a mostrar aquellas que no esten en null, osea que tengan una fecha y por ende ya hayan sido completadas; y que van a estar ordenadas desde la ultima 
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    # va a renderizar tasks, pero va a tener una funcionalidad diferente cuando tenga el datecompleted con una fecha asignada
    return render(request, 'tasks.html', {
        'tasks': tasks,
        'title': 'Completed Tasks'
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


def task_detail(request, task_id):
    # ahora hago la distincion entre get y post para que se ejecute la logica de solo pintar los datos, o actualizar los datos con el POST
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # aca se crea un formulario para actualizar los datos del objeto y que le voy a pasar al frontend: este formularios va a tener precargados los datos de la tarea
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    #  en el else voy a colocar el metodo post, para actualizar la tarea
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            #  esto va a tomar los datos del request.POST, va a generar una instancia, osea un nuevo formulario con los nuevos datos; aqui 'task' se refiere a los datos que coinciden  entre el primary key y el task_id
            form = TaskForm(request.POST, instance=task)
            # guado el nuevo formulario con esos datos.
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task'})
        
# metodo para marcar si la tarea se completo.
def complete_task(request, task_id):
    # si estamos recibiendo una tarea primero tenemos que buscar esa tarea.El modelo de tareas que voy a buscar va a ser Task, y el primary key va a ser el task_id; y le pido las tareas que solo correspondan al usuario
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    # Si el metodo es post voy a tratar de actualizarlo
    if request.method == 'POST':
        # el datecompleted originalmente era null, pero si se le agrega una fecha signifca que ya se cumplio.
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
       
# metodo para eliminar tarea
def delete_task(request, task_id):
    # si estamos recibiendo una tarea primero tenemos que buscar esa tarea.El modelo de tareas que voy a buscar va a ser Task, y el primary key va a ser el task_id; y le pido las tareas que solo correspondan al usuario
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    # Si el metodo es post voy a tratar de actualizarlo
    if request.method == 'POST':
        # a la tarea encontrada, eliminala
        task.delete()
        return redirect('tasks')
       


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
