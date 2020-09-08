from django.urls import path
from authentication import views
urlpatterns = [
    path('', views.home_view, name="home"),
    path("signup/", views.SignUpView.as_view(),
         name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout")
]
