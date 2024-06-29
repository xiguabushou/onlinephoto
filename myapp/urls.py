from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index, name="index"),
    path('photoindex/<int:pIndex>/', views.photoindex, name="photoindex"),
    path('upload/', views.upload, name="upload"),
    path('doupload/', views.doupload, name="doupload"),
    path('delphoto/<int:uid>/', views.delphoto, name="delphoto"),
    path('editpage/<int:uid>/', views.editpage, name="editpage"),
    path('doedit/<int:uid>/', views.doedit, name="doedit"),
    path('login/', views.login, name="login"),
    path('dologin/', views.dologin, name="dologin"),

]