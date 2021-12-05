"""DBproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from MyTree import views

urlpatterns = [
    path('', views.home , name='home'),
    path('showdata' , views.show_data , name = 'showdata'),
    path('insertdata/' , views.insert_data , name = 'insertdata'),
    path('insertdata/insertaction' , views.insert_action , name = 'insertaction') ,
    path('item_detail/<str:id>' , views.item_detail , name = 'item_detail') ,
    path('new_branch/<str:id>/', views.new_branch , name = 'new_branch'),
    path('new_branch/<str:id>/insertaction' , views.insert_branchs , name = 'insertaction') ,
    path('edit_item/<str:id>/', views.edit_item , name = 'edit_item'),
    path('edit_item/<str:id>/updateaction', views.update_item , name = 'updateaction'),
    #path('insertdata' , views.insert_data) ,
    #path('retrievedata/' , views.retrieve_data),
    #path('updatesalary' , views.update_salary),
    #path('deleteentry' , views.delete_entries)
]
