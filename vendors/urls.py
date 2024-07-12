from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register_vendor, name="register_vendor"),
    path("vendors/", views.vendors_page, name="vendor_list"),
    path("vendor/<pk>/", views.vendor_detail, name="vendor_detail"),
    path("login/", views.login, name="login"),
    path("user-guide/", views.user_guide, name="user_guide"),
    path("apply-slot/", views.apply_slot, name="apply_slot"),
    path("blog/", views.blog, name="blog"),
]
