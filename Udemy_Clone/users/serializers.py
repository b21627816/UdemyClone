from rest_framework.serializers import ModelSerializer, ListField
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
        ]


class UserAuthSerializer(ModelSerializer):

    courses = ListField(source='get_all_courses')

    class Meta:
        model = User
        fields = [
            'name',
            'id',
            'courses',
            'email',
        ]
