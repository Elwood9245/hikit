# from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

from .views import event_list

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),

    # route
    path('routes/', views.route_list, name='route_list'),
    path('routes/<int:route_id>/', views.route_detail, name='route_detail'),
    path('routes/<int:route_id>/create-event/', views.create_event, name='create_event'),
    path('routes/<int:route_id>/toggle-save/', views.toggle_save_route, name='toggle_save_route'),
    path('routes/add/', views.add_route, name='add_route'),


    # Events
    path('events/', views.event_list, name='event_list'),

    path('events/<int:event_id>/', views.event_detail, name='event_detail'),

    path('events/<int:event_id>/join/', views.join_event, name='join_event'),
    path('events/<int:event_id>/leave/', views.leave_event, name='leave_event'),

    # User
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),

    # authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)