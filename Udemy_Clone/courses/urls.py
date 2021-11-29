from django.urls import path
from .views import (CoursesHomeView,
                    CourseDetail,
                    SectorCourses,
                    SearchCourse,
                    AddComment,
                    GetCartDetail,
                    CourseStudy,
                    )

urlpatterns = [
    path("<uuid:sector_uuid>/", SectorCourses.as_view(), name="CourseList"),
    path('details/<uuid:course_uuid>/', CourseDetail.as_view(), name="CourseDetails"),
    path('', CoursesHomeView.as_view(), name="CourseHome"),
    path('search/<str:search_term>/',SearchCourse.as_view(), name="SearchCourse"),
    path('comment/<uuid:course_uuid>', AddComment.as_view(), name="AddComment"),
    path('cart/', GetCartDetail.as_view(), name="GetCartDetail"),
    path('study/<uuid:course_uuid>', CourseStudy.as_view(), name="CourseStudy"),
]