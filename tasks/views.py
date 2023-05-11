from django.shortcuts import render, redirect
# userCreationForm es para crear un usuario y AuthenticationForm es para comprobar si el usurio existe.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

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


def signout(request):
    logout(request)
    return redirect('home')

# metodo para que el usuario se pueda autenticas (acceda a sus datos si tiene una cuenta ya creada)
#si la solicitud a esa url es get muestro el formulario, si no, si es una solicutd post, verifico
#si el usuario es none, osea si no existe, mando el error con el formulario, si existe lo envio a la 
#pagina 'tasks' y guardo su session
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
            login(request,user)
            return redirect('tasks')

        
