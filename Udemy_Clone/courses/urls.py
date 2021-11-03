from django.urls import path
from .views import CoursesHomeView

urlpatterns = [
    path('', CoursesHomeView.as_view(),)
]