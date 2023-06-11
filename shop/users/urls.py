from django.urls import path
from users.views import RegisterFormView, UpdateProfile, UserProfile
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path("register/", RegisterFormView.as_view(), name="register"),
    path("update_profile/", UpdateProfile.as_view(), name="update_profile"),
    path("profile/", UserProfile.as_view(), name="profile"),
]