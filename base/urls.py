from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('create-room/', views.createRoom, name="create-room"),
    path('room/<int:pk>', views.room, name="room"),
    path('delete-message/<int:pk>', views.deleteMessage, name="delete-message"),
    path('delete-room/<int:pk>', views.deleteRoom, name="delete-room"),
    path('update-room/<int:pk>', views.updateRoom, name="update-room"),
    path('profile/<int:pk>', views.profile, name="profile"),


    path('topics', views.topic, name="topics"),
    path('activity', views.activity, name="activity"),
    path('login', views.loginPage, name="login"),
    path('logpot', views.logoutPage, name="logout"),
    path('register', views.register, name="register"),
    path('edit-user', views.editUser, name="edit-user"),
]
