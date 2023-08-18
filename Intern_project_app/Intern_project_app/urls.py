"""
URL configuration for Intern_project_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from toDoList import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name='homepage'),
    path('home/',views.home, name='home'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('signup/',views.signup,name='signup'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    path('share_note/<int:note_id>/', views.share_note, name='share_note'),
    path('view_shared_note/<str:token>/', views.view_shared_note, name='view_shared_note'),
    path('homepage/',views.homepage,name='homepage'),
]
