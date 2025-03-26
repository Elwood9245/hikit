from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.template.loader import render_to_string

from .models import Route, Event, Participation, UserProfile, EventComment
from .forms import RouteForm, EventForm, UserProfileForm, EventCommentForm


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
    saved = False
    if request.user.is_authenticated:
        saved = request.user in route.saved_by.all()
    return render(request, 'route.html', {
        'route': route,
        'saved': saved
    })

def create_event(request, route_id):
    route = get_object_or_404(Route, id=route_id)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.route = route
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'create_event.html', {
        'form': form,
        'route': route
    })

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event.objects.prefetch_related('participants'), id=event_id)
    comments = event.comments.filter(parent__isnull=True).order_by('-created_at')
    form = EventCommentForm()
    participation = None

    if request.user.is_authenticated:
        # Check if the user has already joined this event
        participation = Participation.objects.filter(event=event, user=request.user).first()

        # Handle comment submission
        if request.method == 'POST' and 'content' in request.POST:
            form = EventCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.event = event

                # Optional reply to parent comment
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    try:
                        parent = EventComment.objects.get(id=parent_id, event=event)
                        comment.parent = parent
                    except EventComment.DoesNotExist:
                        pass

                comment.save()

                # AJAX response with rendered HTML
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    html = render_to_string('partials/comment_item.html', {
                        'comment': comment,
                        'user': request.user,
                        'event': event,
                    }, request=request)

                    return JsonResponse({
                        'success': True,
                        'message': 'Comment posted!',
                        'comment_html': html
                    })

                return redirect('event_detail', event_id=event.id)

            # If form is invalid and it's an AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': form.errors.as_json()
                }, status=400)

    # Final render
    return render(request, 'event_detail.html', {
        'event': event,
        'form': form,
        'comments': comments,
        'participation': participation,
    })

def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST' and request.user.is_authenticated:
        if not event.participants.filter(user=request.user).exists() and event.can_join:
            Participation.objects.create(
                event=event,
                user=request.user,
                notes=request.POST.get('notes', '')
            )
            event.current_participants += 1
            event.save()
    return redirect('event_detail', event.id)

def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST' and request.user.is_authenticated:
        participation = event.participants.filter(user=request.user).first()
        if participation:
            participation.delete()
            event.current_participants -= 1
            event.save()
    return redirect('event_detail', event.id)

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

@login_required
def profile(request):
    user = request.user

    profile, _ = UserProfile.objects.get_or_create(user=user)

    # Handle profile photo upload (AJAX)
    if request.method == 'POST' and 'profile_picture' in request.FILES:
        profile_pic = request.FILES['profile_picture']
        try:
            # Delete old file if exists
            if profile.profile_picture:
                profile.profile_picture.delete(save=False)


            # Save new file
            profile.profile_picture = profile_pic
            profile.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'profile_picture_url': profile.profile_picture.url,
                    'message': 'Profile photo updated successfully!'
                })
            else:
                # Fallback for non-AJAX (just in case)
                messages.success(request, 'Profile photo updated successfully!')
                return redirect('profile')

        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            else:
                messages.error(request, f'Error: {str(e)}')
                return redirect('profile')

    launched_routes = Route.objects.filter(created_by=user)
    launched_events = Event.objects.filter(organizer=user)
    saved_routes = user.saved_routes.all()  # Adjust depending on your model setup
    participated_events = Event.objects.filter(participants__user=request.user)

    context = {
        'launched_routes': launched_routes,
        'launched_events': launched_events,
        'saved_routes': saved_routes,
        'participated_events': participated_events,
        'profile': profile,
    }
    return render(request, 'profile.html', context)

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # 检查是否还能参加
        if event.can_join and not event.participants.filter(user=request.user).exists():
            Participation.objects.create(
                event=event,
                user=request.user,
                notes=request.POST.get('notes', '')
            )
            event.current_participants += 1
            event.save()

    return redirect('event_detail', event_id=event_id)


@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        participation = event.participants.filter(user=request.user).first()
        if participation:
            participation.delete()
            event.current_participants -= 1
            event.save()

    return redirect('event_detail', event_id=event_id)


@login_required
def toggle_save_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    user = request.user
    if user in route.saved_by.all():
        route.saved_by.remove(user)
        return JsonResponse({'saved': False})
    else:
        route.saved_by.add(user)
        return JsonResponse({'saved': True})

@login_required
def delete_comment(request, event_id, comment_id):
    comment = get_object_or_404(EventComment, id=comment_id, event__id=event_id)

    # Only the comment author can delete
    if comment.user != request.user:
        return render("You are not allowed to delete this comment.")

    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect('event_detail', event_id=event_id)