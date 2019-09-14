from django.urls import path
from .views import home, HomeSinPrivilegios, get_coords
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sin_privilegios', HomeSinPrivilegios.as_view(), name='sin_privilegio'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/login.html'), name='logout'),
    path('grafico/', get_coords, name='grafico'),
    path('', home, name="home"),
]
