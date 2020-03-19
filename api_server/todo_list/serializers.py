from rest_framework import serializers
from .models import Task, Project


class TaskSeriaizer(serializers.HyperlinkedModelSerializer):
    priority = serializers.IntegerField(default=-1)

    class Meta:
        model = Task
        fields = ['text', 'is_done', 'priority', 'deadline', 'url']

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    tasks = TaskSeriaizer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['name', 'owner', 'tasks', 'url']

class TasksReprioritizeSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    up = serializers.BooleanField()

    class Meta:
        fields = ['index', 'up']