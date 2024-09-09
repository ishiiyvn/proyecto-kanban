from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

# Create your views here.
def helloworld(request):
    return HttpResponse('Hola chavales')

def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST[
                'password'])
        if user is None:
            return render(request,'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
