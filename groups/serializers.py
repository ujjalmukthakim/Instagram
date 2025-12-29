from rest_framework import serializers
from .models import MainGroup, SubGroup
from .models import DailyActivity
from .models import WeeklyPost

class MainGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainGroup
        fields = "__all__"


class SubGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubGroup
        fields = "__all__"

class DailyActivitySerializer(serializers.ModelSerializer):
    member_username = serializers.CharField(source='member.username', read_only=True)

    class Meta:
        model = DailyActivity
        fields = '__all__'



class WeeklyPostSerializer(serializers.ModelSerializer):
    member_username = serializers.CharField(source='member.username', read_only=True)
    main_group_name = serializers.CharField(source='main_group.name', read_only=True)

    class Meta:
        model = WeeklyPost
        fields = '__all__'

