
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_vendor, name = "register_vendor"),
    path('', views.homepage, name='homepage'),
    path('vendor/<pk>/', views.vendor_page, name='vendor_page'),
    
]


