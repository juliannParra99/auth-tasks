from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from  django.contrib.auth import login
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
                #login (importado) crea una cookie por nosotros que permite que el navegador guarde datos del usuario en una session: con esos datos guardados, puedo saber por que usuario fueron creadas las tareas, si tiene acceso a determinadas paginas,mostrar la info del usuario, etc.
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