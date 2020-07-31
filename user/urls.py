from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "user"
urlpatterns = [
    path("register/", views.Register.as_view(), name="register"),
    #path('login/', views.Login.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user/<slug:the_slug>/', views.mv_post_by_user, name='mv_post_by_user'),
    path('base/', views.base, name='base'),
]
