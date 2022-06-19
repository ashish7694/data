from django.urls import path
from . import views
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('', views.register, name='register'),
    path('custome_login/', views.custome_login, name='custome_login'),
    # path('signup/', views.sign_up, name='signup'),
    # path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('download/', views.download, name='download'),
    path('logout/', views.user_logout, name='logout'),
    path('update/<int:id>/', views.issues_register_update, name='update'),
    path('sent_email/<str:email>/', views.sent_email, name='sent_email'),
]