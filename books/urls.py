from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path("books", views.show_all),
    path("books/create_book", views.create_book),
    path("books/<int:user_id>", views.show_one),
    path("books/<int:user_id>/update", views.update),
    path("books/<int:user_id>/delete", views.delete),
    path("favorite/<int:user_id>", views.favorite),
    path("unfavorite/<int:user_id>", views.unfavorite),
]