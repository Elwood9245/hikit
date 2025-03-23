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
    route = get_object_or_404(Route, pk=route_id) # 根据主键寻找具体数据
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
    query = request.GET.get('q', '') # q为key对应的value为什么
    if query:
        results = Route.objects.filter(name__icontains=query)  # 一个QuerySet 存储着所有符合条件的对象
    else:
        results = Route.objects.none()
    return render(request, 'search_results.html', {'results': results, 'query': query})

def add_route(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = RouteForm(request.POST, request.FILES)  # Add request.FILES for image upload
        if form.is_valid():
            route = form.save(commit=False)
            route.created_by = request.user
            route.save()
            return redirect('route_detail', route_id=route.id) # 添加完了之后 就重定向到详情的页面
    else:
        form = RouteForm()

    return render(request, 'create_route.html', {'form': form})


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
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
