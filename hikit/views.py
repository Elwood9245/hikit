from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Route, Event
from .forms import RouteForm

def home(request):
    routes = Route.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'routes': routes})

def about(request):
    return render(request, 'about.html')

def route_list(request):
    routes = Route.objects.all()
    return render(request, 'route_list.html', {'routes': routes})

def route_detail(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    return render(request, 'route.html', {'route': route})

def create_event(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    # 处理表单提交逻辑
    return render(request, 'create_event.html', {'route': route})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def profile(request):
    return render(request, 'profile.html')

def search(request):
    query = request.GET.get('q', '')
    results = Route.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})
def add_route(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            route.author = request.user
            route.save()
            return redirect('home')
    else:
        form = RouteForm()

    return render(request, 'route.html', {'form': form, 'action': 'Add'})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
