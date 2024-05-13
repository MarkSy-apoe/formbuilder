from django.urls import path
from . import views
from .views import UserLoginView

urlpatterns = [
    path('register/', views.accountCreate, name="register"),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('account-detail/', views.account, name="account-details"),
    path('forms/', views.form, name="form"),
    path('form/<int:pk>/', views.aform, name="aform"),
    path('preview/<int:pk>/', views.formpreview, name="formpreview"),
    path('components/<int:pk>/', views.formcomponents, name="formcomp"),
    path('component-create/', views.componentcreate, name="compcreate"),
]