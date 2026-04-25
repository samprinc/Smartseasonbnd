# Add this to core/serializers.py
from rest_framework import serializers
from .models import Field, FieldUpdate
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role'] # Only send what is needed!

class FieldUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldUpdate
        fields = ['id', 'field', 'created_at', 'notes', 'stage_at_update']

class FieldSerializer(serializers.ModelSerializer):
    # Included calculated field for status
    agent_name = serializers.CharField(source='assigned_to.username', read_only=True)
    current_status = serializers.CharField(read_only=True)
    updates = FieldUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Field
        fields = ['id', 'name', 'crop_type', 'planting_date', 'stage', 'assigned_to', 'current_status', 'updates', 'agent_name']