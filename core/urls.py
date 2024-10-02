
from django.urls import path
from . import views


# URLConf
urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login, name="login"),
    path('register/', views.register , name="register"),
    path('logout/', views.logout , name="logout"),
    path('upload/', views.upload_csv, name="upload"),
    path('query-builder/', views.build_query, name="query_builder"),
    path('users/', views.manage_users, name="users"),
]
