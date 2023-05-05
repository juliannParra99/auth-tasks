from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def helloworld(request):
    title = 'Hello world'
    return render(request, 'signup.html', {
        'form':UserCreationForm
    })