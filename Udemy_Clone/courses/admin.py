from django.contrib import admin
from .models import Course, Sector, Episode, CourseSection, Comment

# Register your models here.


admin.site.register(Course)
admin.site.register(CourseSection)
admin.site.register(Sector)
admin.site.register(Episode)
admin.site.register(Comment)