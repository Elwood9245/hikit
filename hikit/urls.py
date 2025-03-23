# from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),

    # route
    path('routes/', views.route_list, name='route_list'),
    path('route/<int:route_id>/', views.route_detail, name='route_detail'),
    path('route/<int:route_id>/create-event/', views.create_event, name='create_event'),
    path('routes/add/', views.add_route, name='add_route'),

    # Events
    path('events/', views.event_list, name='event_list'),

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