"""
URL configuration for webinterface project.

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
from django.urls import path
from myapp.views import login, login_page, logout, contact, start_task, finish_task, employee_page, manager_page

urlpatterns = [
    path('', login_page, name='login_page'),
    path('login/', login_page, name='login_page'),
    path('login/authenticate/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('start_task/', start_task, name='start_task'),
    path('finish_task/', finish_task, name='finish_task'),
    path('employee_page/', employee_page, name='employee_page'),
    path('manager_page/', manager_page, name='manager_page'),
]
