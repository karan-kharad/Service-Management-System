from django.urls import path
from . import views
urlpatterns = [
    path('job/',views.JobListView.as_view()),
    # path('jobinfo/', views.JobInfoView.as_view),
    path('job/<int:pk>/', views.JobDetilsView.as_view()),
    path('customer/', views.CustomerListView.as_view()),
    path('user/', views.UserListView.as_view()),
    path('user-job/', views.UserJobListView.as_view()),
]