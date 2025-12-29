from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    role = serializers.CharField(read_only=True, default='Member')  # Force Member role

    class Meta:
        model = User
        fields = ['username', 'password', 'instagram_username', 'instagram_url',
                  'custom_password', 'main_group', 'sub_group', 'role']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            instagram_username=validated_data.get('instagram_username', ''),
            instagram_url=validated_data.get('instagram_url', ''),
            custom_password=validated_data.get('custom_password', ''),
            main_group=validated_data.get('main_group', ''),
            sub_group=validated_data.get('sub_group', ''),
            role='Member',  # Force Member role
            status='Pending'  # Pending approval by default
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
