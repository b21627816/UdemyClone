from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Sector
from .serializers import CourseDisplaySerializer
# Create your views here.


class CoursesHomeView(APIView):

    def get(self, request, *args, **kwargs):
        sectors = Sector.objects.order_by("?")

        sector_response = []

        for sector in sectors:
            sector_courses = sector.related_course.order_by("?")[:4]
            course_Serializer = CourseDisplaySerializer(sector_courses, many=True)

            sector_obj = {
                "sector_name": sector.sector_title,
                "sector_uuid": sector.sector_uuid,
                "featured_courses": course_Serializer.data,
                "sector_image": sector.get_image_absolute_url()
            }

            sector_response.append(sector_obj)

        return Response(data=sector_response, status = status.HTTP_200_OK)