from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('quotes', views.success),
    path('logout', views.logout),
    path('uploadquote', views.uploadquote),
    path('addtofavorites/<quote_id>', views.addtofavorites),
    path('removefromfavorites/<quote_id>', views.removefromfavorites),
    path('delete/<quote_id>', views.delete),
    path('quotes/<quote_id>', views.editpage),
    path('edit/<quote_id>', views.edit),
    path('user/<user_id>', views.posts),
    ]