from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, TaskForm
from django.contrib.auth import authenticate, login, logout
from .models import Task

# Create your views here.
def home(request):
    form  = TaskForm()
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        user = request.user

        Task.objects.create(
            user = user,
            name = name,
            description = description,
        )

        return redirect('home')

    tasks = None
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    context = {}
    context['tasks'] = tasks
    return render(request, 'base/home.html', context)

def task_desc(request, pk):
    task = Task.objects.get(id=int(pk))
    context = {}
    context['task'] = task
    return render(request, 'base/task_desc.html', context)

def update_task(request, pk):
    task = Task.objects.get(id=int(pk))
    task.completed = not task.completed
    task.save()
    return redirect('home')

def delete_task(request, pk):
    task = Task.objects.get(id=int(pk))
    task.delete()
    return redirect('home')

def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CustomUserCreationForm()
    context = {}
    context['form'] = form
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'base/login_page.html', context)

    return render(request, 'base/register_page.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    context = {}
    return render(request, 'base/login_page.html', context)

def logout_page(request):
    logout(request)
    return redirect('login')