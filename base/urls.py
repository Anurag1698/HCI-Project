from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("", views.home, name="home"),
    path("rooms/", views.rooms, name="rooms"),
    path("room/<str:pk>/", views.room, name="room"),
    path("profile/<str:pk>/", views.userProfile, name="user-profile"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:pk>/", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="delete-room"),
    path("room/<str:pk>/joinUs/", views.joinUs, name="joinUs"),
    # path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
    path(
        "room/<int:room_id>/manage-requests/",
        views.manage_room_requests,
        name="manage-room-requests",
    ),
    path("update-user/", views.updateUser, name="update-user"),
    path("blogs/", views.blogs, name="blogs"),
    path("blog/<str:pk>/", views.blog, name="blog"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("service/", views.service, name="service"),
    path("faq/", views.faq, name="faq"),
    path(
        "room/<int:room_id>/remove-participant/<int:user_id>/",
        views.kick_participant,
        name="remove-participant",
    ),
]
