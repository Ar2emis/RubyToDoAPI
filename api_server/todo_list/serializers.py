from rest_framework import serializers
from .models import Task, Project


class TaskSeriaizer(serializers.HyperlinkedModelSerializer):
    priority = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = ['text', 'is_done', 'priority', 'deadline', 'url']

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    tasks = TaskSeriaizer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['name', 'owner', 'tasks', 'url']

class TasksReprioritizeSerializer(serializers.Serializer):
    priorities = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        fields = ['priorities']