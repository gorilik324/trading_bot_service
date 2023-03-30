from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.RegisterViewSet.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('me/', views.MeView.as_view(), name='profile')
]
