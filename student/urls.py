from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('register/', views.register_for_events, name='register_for_events'),
    path('my/', views.my_participations, name='my_participations'),
    path('logout/', views.logout_view, name='logout'),
]