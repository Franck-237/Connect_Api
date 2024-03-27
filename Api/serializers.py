from rest_framework import serializers
from TodoList.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'completed'
        ]

class TodoToggleCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = [
                'title',
                'description',
                'created_at',
                'completed'
            ]