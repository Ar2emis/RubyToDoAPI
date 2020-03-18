from .serializers import TaskSeriaizer, ProjectSerializer, TasksReprioritizeSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Task
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import OrderingFilter


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = ProjectSerializer
    task_serializer_class = TaskSeriaizer
    reprioritaze_serializer_class = TasksReprioritizeSerializer

    def get_queryset(self):
        token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]

        user = Token.objects.get(key=token).user

        queryset = Project.objects.filter(owner=user)

        return queryset

    def get_serializer_class(self):
        if self.action == 'add_task':
            return self.task_serializer_class
        elif self.action == 'reprioritize':
            return self.reprioritaze_serializer_class
        else:
            return super(ProjectViewSet, self).get_serializer_class()

    @action(detail=True, methods=['post'])
    def add_task(self, request, pk=None):
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        project = self.get_object()

        serializer.save()

        task = serializer.instance
        task.priority = len(project.tasks.all())

        project.tasks.add(task)

        data = self.serializer_class(instance=project, context={'request': request}).data

        self.sort_tasks(data)

        return Response(data=data, status=status.HTTP_200_OK)

    def sort_tasks(self, project):
        project['tasks'] = sorted(project['tasks'], key=lambda task: task['priority'])

    def sort_projects_tasks(self, projects):
        for project in projects:
            self.sort_tasks(project)

    def list(self, request):
        response = super(ProjectViewSet, self).list(request)

        if response.status_code != status.HTTP_200_OK:
            return response

        data = response.data

        self.sort_projects_tasks(data)

        response.data = data

        return response

    def retrieve(self, request, pk=None):
        response = super(ProjectViewSet, self).retrieve(request, pk)

        if response.status_code != status.HTTP_200_OK:
            return response

        data = response.data

        self.sort_tasks(data)

        response.data = data

        return response

    def perform_create(self, serializer):
        token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]

        user = Token.objects.get(key=token).user

        serializer.save(owner=user)



    @action(detail=True, methods=['post'])
    def reprioritize(self, request, pk=None):
        serializer = self.get_serializer_class()(data=self.request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        priorities = serializer.data['priorities']

        project = self.get_object()
        tasks = project.tasks.all()

        for task in tasks:
            task.priority = priorities.index(task.priority)
            task.save()

        data = self.serializer_class(instance=project, context={'request': request}).data

        self.sort_tasks(data)

        return Response(data=data, status=status.HTTP_200_OK)

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = TaskSeriaizer
    queryset = Task.objects.all()
