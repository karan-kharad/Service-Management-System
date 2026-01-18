from django.urls import path
from . import views
urlpatterns = [
    path('job/', views.job_list),
    path('job/<int:pk>/', views.job_detils),
    path('customer/', views.customer_list),
    path('user/', views.user_list),
]